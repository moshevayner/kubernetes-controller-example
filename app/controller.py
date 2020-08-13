#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from config import Config
from lib.clients.k8s import K8sClient
from lib.pod_builder import PodBuilder

api_group = Config.api_group
plural = Config.examples_plural
version = Config.examples_version

k8s = K8sClient()
pod_builder = PodBuilder(namespace=Config.namespace)


def handle_event(event):
    """
    This method receives an event, checks for its type and passes it to the relevant method for handling
    :param event: event to handle
    """
    obj = event["object"]

    if event["type"] == "ERROR":
        if event["object"].get("message") and "too old resource version" in event["object"]["message"]:
            # Known issue, no harm. https://github.com/kubernetes/kubernetes/issues/22024
            pass
        else:
            logging.error("Received ERROR event from Kubernetes API: {}".format(event))
    elif event["type"] == "ADDED":
        logging.debug("{} - {}".format(event["type"], obj["metadata"]["name"]))
        handle_added_example(obj)
    elif event["type"] == "DELETED":
        logging.debug("{} - {}".format(event["type"], obj["metadata"]["name"]))
        pass
    elif event["type"] == "MODIFIED":
        logging.debug("{} - {}".format(event["type"], obj["metadata"]["name"]))
        handle_modified_example(obj)
    else:
        logging.error("Unhandled event: {}".format(obj))


def handle_added_example(example):
    """
    This will handle an event of an added resource that is relevant for our controller
    :param example: example to handle
    """
    if example['spec']['podName'] != 'Unassigned':
        logging.debug('Pod already created for example, ignoring..')
    else:
        pod_name = pod_builder.build_example_pod(example)
        logging.info(f'Created pod: {pod_name} for example: {example["metadata"]["name"]}')
        k8s.patch_example(
            name=example['metadata']['name'],
            namespace=Config.namespace,
            body={'spec': {'podName': pod_name}}
        )


def handle_modified_example(example):
    """
    This will handle an event of a modified resource that is relevant for our controller
    :param example: example to handle
    """
    # Here we will implement any method we'd like to handle a case in which an example CR was modified.
    pass


def main():
    logging.basicConfig(level=Config.log_level, stream=sys.stdout,
                        format='%(asctime)s %(levelname)s: %(message)s')
    logging.info('===== Hello K8s Controller is now running! =====')
    logging.info(f'== Current version: {Config.version} ==')
    k8s.confirm_crd_access(group=Config.api_group, version=Config.examples_version, plural=Config.examples_plural)
    while True:
        for event in k8s.watch_custom_objects(
                group=Config.api_group,
                version=Config.examples_version,
                plural=Config.examples_plural,
                timeout_seconds=300
        ):
            handle_event(event)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import kubernetes
from kubernetes.client.rest import ApiException
from config import Config

logger = logging.getLogger(__name__)


def _authenticate(method):
    if method == "cluster":
        kubernetes.config.load_incluster_config()
    elif method == "local":
        kubernetes.config.load_kube_config()
    elif method == "test":
        pass
    else:
        raise Exception("Invalid authentication method. Should be either cluster or local.")


class K8sClient:
    def __init__(self, authentication=Config.auth_method):
        _authenticate(authentication)
        self.core_api = kubernetes.client.CoreV1Api()
        self.custom_obj_api = kubernetes.client.CustomObjectsApi()
        self.ApiException = kubernetes.client.rest.ApiException

    def confirm_crd_access(self, group, version, plural):
        try:
            self.custom_obj_api.list_cluster_custom_object(group=group, version=version, plural=plural)
        except kubernetes.client.rest.ApiException as err:
            logger.error(f"Unable to retrieve {plural} from Kubernetes API. Received the following error: {err}")
            sys.exit(100)

    def create_pod(self, namespace, body):
        self.core_api.create_namespaced_pod(namespace=namespace, body=body)

    def patch_example(self, name, namespace, body):
        self.custom_obj_api.patch_namespaced_custom_object(name=name,
                                                           namespace=namespace,
                                                           body=body,
                                                           plural=Config.examples_plural,
                                                           group=Config.api_group,
                                                           version=Config.examples_version)

    def watch_custom_objects(self, group, version, plural, **kwargs):
        watcher = kubernetes.watch.Watch()
        return watcher.stream(self.custom_obj_api.list_cluster_custom_object, group, version, plural, **kwargs)


def main():
    pass


if __name__ == "__main__":
    main()

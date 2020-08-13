#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from kubernetes import client
from lib.clients.k8s import K8sClient


class PodBuilder:
    def __init__(self, namespace):
        self.k8s_client = K8sClient()
        self.namespace = namespace

    def build_example_pod(self, example):
        pod_name = f'{example["metadata"]["name"]}-{datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]}'
        example_name = example['metadata']['name']
        self.k8s_client.create_pod(namespace=self.namespace, body=self.__generate_example_pod_body(pod_name, example_name))
        return pod_name

    def __generate_example_pod_body(self, name, example_name):
        metadata = client.V1ObjectMeta(
            labels={'app': 'example', 'example-name': example_name},
            name=name,
            namespace=self.namespace
        )
        container = client.V1Container(
            command=['/bin/bash', '-c', 'while true; do echo "$(date) Hello, k8s!"; sleep 10 ; done'],
            image='debian:10-slim',
            name='example'
        )
        spec = client.V1PodSpec(
            containers=[container],
            termination_grace_period_seconds=2
        )
        pod = client.V1Pod(metadata=metadata, spec=spec)
        return pod


def main():
    pass


if __name__ == "__main__":
    main()

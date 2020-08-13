#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class Config:
    api_group = os.environ.get('API_GROUP', 'hello-k8s.s5t.dev')
    auth_method = os.environ.get("AUTH_METHOD", "cluster")
    examples_plural = os.environ.get('API_PLURAL', 'examples')
    examples_version = os.environ.get('API_VERSION', 'v1alpha1')
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    namespace = os.environ.get('NAMESPACE', 'default')
    version = '1.0.0'


def main():
    pass


if __name__ == "__main__":
    main()

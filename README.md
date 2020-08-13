# kubernetes-controller-example
Hello, Kubernetes!

### Purpose
This repository contains a super basic example for a custom kubernetes controller.
The controller watches for new custom resources of kind `example` in the `hello-k8s.s5t.dev` apiGroup.
Whenever a new `example` resource is created, the controller will spin-up a one-off pod which will simply print a `date` timestamp along
with the famous `hello, world` example, only this one would say `hello, k8s!`.
The entire code is written in Python and utilizies the [official Python client for Kubernetes](https://github.com/kubernetes-client/python)
for any interaction with the Kubernetes API.

### Running the controller
In order to run this example controller, you may either apply the provided manifests in [k8s-manifests](k8s-manifests) to your cluster (`kubectl apply -f k8s-manifests/`)
Or simply run this controller locally on your machine. If you have Python3 installed, you may run `python -u controller.py`, or if you prefer the containerized way, you may build the docker image locally and run it, or simply pull 
the [pre-built image from Dockerhub](https://hub.docker.com/r/mosheshi/kubernetes-controller-example) which updates the `latest` tag with every new update to this repository.
**NOTE** - if you are running the controller on your local machine rather than in your cluster, you'll have to have:
1. A working `.kube/config` file pointing to the cluster in which you'd like to test this (`current-context` should point to the desired cluster).
2. Include the following environment variable in your controller runtime environment (either containerized or local) = `AUTH_METHOD=local`. This instructs the k8s client to pull the kubernetes api connection information from your local `.kube/config` file rather than the default `cluster` authentication method.
(More information about this can bee seen in the [k8s client authentication method](app/lib/clients/k8s.py)), under `_authenticate` function. 
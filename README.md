# WES Factory Agent

This project creates a docker image (intended to be used in k3s) that publishes factory specific information.  This project is **only** intended to be run in a "factory" environment and should **not** be run in production.

## Data Published

The following data is published to both Beehive and inter-node.

- `sys.net.ip`: the network interface IP addresses

## How to Run on a Node

On the node that is to run this container:

```
kubectl apply -f wes-factory.yaml
```

or

```
kubectl apply -f <github wes-factory URL to /wes-factory.yaml>
```

## Configuration

The interfaces to publish IP addresses for is controlled by the `INTERFACES` environment variable defined in `wes-factory.yaml`.

Other configurations (such as "publish scope") can be specified from the `Dockerfile`.  See `main.py` possible arguments for details.

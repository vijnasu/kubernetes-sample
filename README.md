# kubernetes-sample
Kubernetes Python GRPC based Client Server Service Sample

In this example, we'll deploy a gRPC server and client, both written in Python. Here's a simplified example of what those might look like.

## 1. gRPC Server (server.py):

```python
from concurrent import futures
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
```

## 2. gRPC Client (client.py):

```python
import grpc
import helloworld_pb2
import helloworld_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()
```

First, we will create Dockerfiles for both server and client:

## 3. Dockerfile for server:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Proxy setting to be added here
# ToDo: http_proxy, https_proxy

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org grpcio-tools

# Run server.py when the container launches
CMD ["python", "server.py"]
```

## 4. Dockerfile for client:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org grpcio-tools

# Run client.py when the container launches
CMD ["python", "client.py"]
```

Next, we need to build and push these images to a Docker registry. Docker Hub, Google Container Registry, or a private registry can be used. We are using local registry.

```bash
# Build Server Image
docker build -t grpc-server:latest server/

# Build Client Image
docker build -t grpc-client:latest client/
```

Finally, we can deploy these applications to Kubernetes:

## 5. Kubernetes Deployment for server:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grpc-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grpc-server
  template:
    metadata:
      labels:
        app: grpc-server
    spec:
      containers:
      - name: grpc-server
        image: grpc-server:latest
        ports:
        - containerPort: 50051
---
apiVersion: v1
kind: Service
metadata:
  name: grpc-server
spec:
  type: NodePort
  selector:
    app: grpc-server
  ports:
      - protocol: TCP
        port: 50051
        targetPort: 50051
```

## 6. Kubernetes Deployment for client:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grpc-client
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grpc-client
  template:
    metadata:
      labels:
        app: grpc-client
    spec:
      containers:
      - name: grpc-client
        image: grpc-client:latest
```

After creating these deployments, you can apply them using **kubectl apply -f server-deployment.yaml** and **kubectl apply -f client-deployment.yaml**.

If everything is set up correctly, the client will be able to communicate with the server within the Kubernetes cluster. Remember to replace localhost with **grpc-server** in the client.py file so it can discover the server via Kubernetes service discovery. We also need to ensure that our Python server and client use the correct gRPC API definitions (the helloworld_pb2 and helloworld_pb2_grpc files in the example). Those would be generated from a .proto

Here's an example of what a .proto file might look like:

**helloworld.proto:**

```
syntax = "proto3";

package helloworld;

// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
```

After creating the helloworld.proto file, you can generate the helloworld_pb2.py and helloworld_pb2_grpc.py files with the following command:

```
python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./helloworld.proto
```

This command will generate the **helloworld_pb2.py** and **helloworld_pb2_grpc.py** files in the current directory (.). The -I./ argument tells protoc where to look for imports. The --python_out and --grpc_python_out options tell protoc where to output the generated Python files.

After we've run this command, we should see the helloworld_pb2.py and helloworld_pb2_grpc.py files in our current directory, and we should be able to import them in our server.py file.

Remember to run this command every time we update the .proto file to ensure the Python files are up-to-date.

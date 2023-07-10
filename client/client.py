import os
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

def run():
    server = os.getenv('SERVER_NAME', 'grpc-server')
    port = os.getenv('SERVER_PORT', '32000')
    with grpc.insecure_channel(f'{server}:{port}') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)

if __name__ == '__main__':
    run()

import os
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

def run():
    server = os.getenv('GRPC_SERVER_SERVICE_HOST', 'grpc-server')
    port = os.getenv('GRPC_SERVER_SERVICE_PORT', '32000')
    with grpc.insecure_channel(f'{server}:{port}') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)

if __name__ == '__main__':
    run()

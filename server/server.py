import os
from concurrent import futures
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

def serve():
    port = os.getenv("SERVER_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

import socket
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import uuid
import socketserver
from Sockets import ThreadedTCPRequestHandler, ThreadedTCPServer, send_msg_func, create_msg
import json
from Functions import func_per_second, check_within_range, get_distance


class Node:

    def __init__(self, x, y, dx, dy, range_radius=50):
        self.id = uuid.uuid4()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.range = range_radius
        self.server = None
        self.start_server()

    def get_pos(self):
        return {'x': self.x, 'y': self.y}

    def get_velocity(self):
        return {'dx': self.dx, 'dy': self.dy}

    def set_velocity(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def start_server(self):
        HOST, PORT = "localhost", 0

        self.server = ThreadedTCPServer(
            (HOST, PORT), ThreadedTCPRequestHandler)
        print(f"Server started on port: {self.server.server_address[1]}")
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

    def stop_server(self):
        self.server.shutdown()

    def send_msg(self, recv_addr, msg):

        if recv_addr != ('', 0):
            with ThreadPoolExecutor() as executor:
                send_msg_thread = executor.submit(
                    send_msg_func, recv_addr, msg)
                # print(send_msg_thread.result())

    def stop_moving(self):
        self.dx = 0
        self.dy = 0

    def move(self):
        self.x += self.dx
        self.y += self.dy
        print(
            f"Node {self.server.server_address[1]} moved to {self.x} {self.y}"
        )


class StaticNode(Node):

    def __init__(self, x, y, range_radius=50):
        super().__init__(x, y, 0, 0, range_radius)


if __name__ == "__main__":
    nodes = [Node(0, 0, 0, 0) for _ in range(2)]
    staticnodes = [StaticNode(0, 0) for _ in range(2)]

    nodes[0].send_msg(nodes[1].server.server_address,
                      create_msg(nodes[0].server.server_address, "Hi"))
    nodes[1].send_msg(staticnodes[0].server.server_address,
                      create_msg(nodes[1].server.server_address, "Hi"))
    staticnodes[0].send_msg(staticnodes[1].server.server_address,
                            create_msg(staticnodes[0].server.server_address, "Hi"))

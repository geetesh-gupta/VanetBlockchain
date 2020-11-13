import socket
import threading
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import uuid
import socketserver
from Sockets import ThreadedTCPRequestHandler, ThreadedTCPServer, send_msg_func, create_msg
import json
from Functions import func_per_second, check_within_range, get_distance
from Crypto.PublicKey import RSA


class Node:

    def __init__(self, x, y, dx, dy, range_radius=70):
        self.id = None
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.range = range_radius
        self.server = None
        self._private_key = None
        self.nearby_nodes = set()
        self.start_server()
        self.authenticate()

    def get_pos(self):
        return {'x': self.x, 'y': self.y}

    def get_velocity(self):
        return {'dx': self.dx, 'dy': self.dy}

    def reverse_direction(self):
        self.dx = -self.dx
        self.dy = -self.dy

    def set_velocity(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def start_server(self):
        HOST, PORT = "localhost", 0

        self.server = ThreadedTCPServer(
            (HOST, PORT), ThreadedTCPRequestHandler)
        self.server.node = self
        # print(f"Server started on port: {self.server.server_address[1]}")
        self.id = self.server.server_address[1]
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
        # print(
        #     f"Node {self.server.server_address[1]} moved to {self.x} {self.y}"
        # )

    def reset_nearby_nodes(self):
        self.nearby_nodes = set()

    def add_nearby_node(self, node):
        self.nearby_nodes.add(node)

    def authenticate(self):
        private_key = RSA.generate(2048)
        self._private_key = private_key
        self.add_public_key_to_vca(private_key.publickey())

    def add_public_key_to_vca(self, key):
        with open(f'vca/{self.id}.txt', 'wb') as f:
            f.write(key.export_key())

    @staticmethod
    def retrieve_public_key(node_id):
        with open(f'vca/{node_id}.txt', 'rb') as f:
            return RSA.import_key(f.read())

    def __del__(self):
        if os.path.exists(f'vca/{self.id}.txt'):
            os.remove(f'vca/{self.id}.txt')


class StaticNode(Node):

    def __init__(self, x, y, range_radius=50):
        super().__init__(x, y, 0, 0, range_radius)


class Accident(StaticNode):

    def __init__(self, x, y):
        super().__init__(x, y, 0)


if __name__ == "__main__":
    nodes = [Node(0, 0, 0, 0) for _ in range(2)]
    staticnodes = [StaticNode(0, 0) for _ in range(2)]

    nodes[0].send_msg(nodes[1].server.server_address,
                      create_msg(nodes[0].server.server_address, "Hi"))
    nodes[1].send_msg(staticnodes[0].server.server_address,
                      create_msg(nodes[1].server.server_address, "Hi"))
    staticnodes[0].send_msg(staticnodes[1].server.server_address,
                            create_msg(staticnodes[0].server.server_address, "Hi"))

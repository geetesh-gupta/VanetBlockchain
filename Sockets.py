import socketserver
import threading
import socket
import json


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        data = json.loads(data)
        print(
            f"Node {self.request.getsockname()[1]} received {data['msg']} from node {data['server_address'][1]}")
        # cur_thread = threading.current_thread()
        # response = bytes(f"{data}", 'ascii')
        # self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def send_msg_func(recv_address, msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(recv_address)
    try:
        sock.sendall(bytes(msg, 'ascii'))
        data = json.loads(msg)
        print(
            f"Node {data['server_address'][1]} sent {data['msg']} to {recv_address[1]}")
        response = str(sock.recv(1024), 'ascii')
        if response:
            print("Received response from {}".format(response))
    finally:
        sock.close()


def create_msg(server_address, msg):
    return json.dumps({
        "server_address": server_address,
        "msg": msg
    })


if __name__ == "__main__":
    send_msg_func(('localhost', int(input())), "HI")

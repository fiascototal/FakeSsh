import socket
from fake_ssh import config


class FakeSshServer(object):
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((config.NETWORK_INTERFACE, config.NETWORK_TCP_PORT))

    def run(self):
        self._sock.listen(100)
        print("Listening for connection ...")

        while True:
            client, addr = self._sock.accept()
            (client_ip, client_port) = addr
            print("Got a connection from %s:%d" % (client_ip, client_port))

import socket
import datetime
from fake_ssh import config
from fake_ssh.database import connect, create_tables, DbIp, DbUsername, DbPassword, DbBanned, DbValidAccount, DbLog


class FakeSshServer(object):
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((config.NETWORK_INTERFACE, config.NETWORK_TCP_PORT))
        connect()
        create_tables()

    def start(self):
        self._sock.listen(100)
        print("Listening for connection ...")

        while True:
            client, addr = self._sock.accept()
            (client_ip, client_port) = addr
            print("Got a connection from %s:%d" % (client_ip, client_port))

            if FakeSshServer.is_ban(client_ip):
                print("This client is still ban")
                continue

    @staticmethod
    def is_ban(ip_addr):
        if DbIp.select().where(DbIp.value == ip_addr).count() == 0:
            return False
        ip_obj = DbIp.get(value=ip_addr)
        for ban in DbBanned.select().where(DbBanned.ip == ip_obj):
            if ban.date + datetime.timedelta(days=ban.duration) > datetime.datetime.now():
                return True
        return False

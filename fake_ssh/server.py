import socket
import datetime
import paramiko
import threading
from fake_ssh import config
from fake_ssh.database import connect, create_tables, DbIp, DbUsername, DbPassword, DbBanned, DbValidAccount, DbLog


class FakeSsh(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        print("username: %s" % username)
        print("password: %s" % password)
        return paramiko.AUTH_FAILED


class SshClient(threading.Thread):
    def __init__(self, client, addr, host_key):
        super().__init__()
        self._client = client
        self._addr = addr
        self._host_key = host_key

    def run(self):
        t = paramiko.Transport(self._client)
        t.add_server_key(self._host_key)

        server = FakeSsh()
        try:
            t.start_server(server=server)
        except paramiko.SSHException:
            print("*** SSH negotiation failed.")
            t.close()
            return

        # wait for auth
        chan = t.accept(20)
        if chan is None:
            print("*** No channel.")
            t.close()
            return
        print("Authenticated!")
        chan.close()


class FakeSshServer(object):
    def __init__(self, config_filename=""):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((config.NETWORK_INTERFACE, config.NETWORK_TCP_PORT))

        # load config
        config.load_config(config_filename)

        # sqlite database
        connect()
        create_tables()

        # generate a key
        self._host_key = None
        self.generate_key()

        self._clients = []

    def generate_key(self, key_type, key_size):
        if key_type == "rsa":
            print("Generate RSA key (%d bits)" % key_size)
            self._host_key = paramiko.RSAKey.generate(key_size)
        elif key_type == "dsa":
            print("Generate DSA key (%d bits)" % key_size)
            self._host_key = paramiko.DSSKey.generate(key_size)
        else:
            raise Exception("invalid key type: %s" % key_type)
        print("Done (fingerprint: %s)" % self._host_key.get_fingerprint())

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

            new_client = SshClient(client, addr, self._host_key)
            new_client.start()

            self._clients.append(new_client)

    @staticmethod
    def is_ban(ip_addr):
        if DbIp.select().where(DbIp.value == ip_addr).count() == 0:
            return False
        ip_obj = DbIp.get(value=ip_addr)
        for ban in DbBanned.select().where(DbBanned.ip == ip_obj):
            if ban.date + datetime.timedelta(days=ban.duration) > datetime.datetime.now():
                return True
        return False

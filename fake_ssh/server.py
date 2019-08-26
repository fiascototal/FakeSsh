import time
import socket
import datetime
import paramiko
import threading
from fake_ssh import config
from fake_ssh.database import DbIp, DbUsername, DbPassword, DbBanned, DbLog
from fake_ssh.client import FakeSshClient

__version__ = "1.0"


class FakeSsh(paramiko.ServerInterface):
    def __init__(self, ip_addr):
        self._ip_obj = DbIp.get(value=ip_addr)

    def check_auth_password(self, username, password):
        print("[+] got a login try: %s - %s - %s" % (self._ip_obj.value, username, password))

        username_obj, is_created = DbUsername.get_or_create(name=username)
        if is_created:
            print("[+] new username: %s" % username_obj.name)

        password_obj, _ = DbPassword.get_or_create(pwd=password)

        DbLog.create(
            ip=self._ip_obj,
            username=username_obj,
            password=password_obj,
        )

        if config.SLOW_MILLISEC > 0:
            time.sleep(config.SLOW_MILLISEC / 1000000.0)

        back_client = FakeSshClient(self._ip_obj.value, username, password)
        back_client.start()

        return paramiko.AUTH_FAILED

    def get_banner(self):
        lang = "en-US"
        banner = "SSH honeypot with auto login back (version: %s)" % __version__
        return banner, lang


class SshClient(threading.Thread):
    def __init__(self, client, ip_addr, host_key):
        super().__init__()
        self._client = client
        self._host_key = host_key
        self._ip_addr = ip_addr
        self._ssh_obj = FakeSsh(ip_addr=ip_addr)

    def run(self):
        try:
            t = paramiko.Transport(self._client)
            t.add_server_key(self._host_key)

            try:
                t.start_server(server=self._ssh_obj)
            except paramiko.SSHException:
                print("  [-] SSH negotiation failed.")
                t.close()
                return

            # wait for auth
            chan = t.accept(20)

            # we don't care about the result of accept because we will close the connection after all
            if chan:
                chan.close()
            t.close()

            print("  [+] connection closed")

            # now we check if we need to ban this client
            self.check4ban()

        except Exception as err:
            print("  [-] Error: %s" % err)

    def check4ban(self):
        ip_obj = DbIp.get(value=self._ip_addr)

        if DbLog.select().where(
                DbLog.ip == ip_obj,
                DbLog.date > datetime.datetime.now() - datetime.timedelta(days=config.BAN_LIMIT_PERIOD)
        ).count() > config.BAN_LIMIT:
            print("[!] ban ip %s" % self._ip_addr)
            DbBanned.create(ip=self._ip_addr, duration=config.BAN_DAY_MAX)


class FakeSshServer(object):
    def __init__(self):
        print("[+] fake ssh server started")

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((config.NETWORK_INTERFACE, config.NETWORK_TCP_PORT))

        # generate a key
        self._host_key = None
        self.generate_key(config.CRYPTO_KEY_TYPE, config.CRYPTO_KEY_SIZE)

        self._clients = []

    def generate_key(self, key_type, key_size):
        if key_type == "rsa":
            print("[+] Generate RSA key (%d bits)" % key_size)
            self._host_key = paramiko.RSAKey.generate(bits=key_size)
        elif key_type == "dsa":
            print("[+] Generate DSA key (%d bits)" % key_size)
            self._host_key = paramiko.DSSKey.generate(bits=key_size)
        else:
            raise Exception("invalid key type: %s" % key_type)
        print("  [+] fingerprint: %s" % (":".join(["%02X" % x for x in self._host_key.get_fingerprint()])))

    def start(self):
        self._sock.listen(100)

        while True:
            print("[+] Listening for connection ...")
            client, addr = self._sock.accept()

            (client_ip, client_port) = addr
            print("[+] Got a connection from %s:%d" % (client_ip, client_port))

            ip_obj, is_created = DbIp.get_or_create(value=client_ip)
            if is_created:
                print("[+] new ip: %s" % ip_obj.value)

            if FakeSshServer.is_ban(client_ip):
                print("[-] This client is still ban")
                continue

            new_client = SshClient(client, client_ip, self._host_key)
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

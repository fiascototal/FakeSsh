import threading
import paramiko
from fake_ssh.database import DbValidAccount, DbIp, DbUsername, DbPassword


class FakeSshClient(threading.Thread):

    def __init__(self, hostname, username, password):
        super().__init__()
        self._hostname = hostname
        self._username = username
        self._password = password

    def run(self):
        print("[+] connect back to %s using %s:%s" % (self._hostname, self._username, self._password))

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(
                hostname=self._hostname,
                port=22,
                username=self._username,
                password=self._password,
                timeout=10)
        except Exception as err:
            print("  [-] connection failed: %s" % err)
            return

        print("  [+] connection success")
        client.close()

        self.add_valid_account()

    def add_valid_account(self):
        ip_obj = DbIp.get(value=self._hostname)
        username_obj = DbUsername.get(name=self._username)
        password_obj = DbPassword.get(pwd=self._password)
        DbValidAccount.create(
            ip=ip_obj,
            username=username_obj,
            password=password_obj
        )

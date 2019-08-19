import os
import configparser


"""
example of INI file:

[general]
slow_millisec=500
sqlite_path=logs.db

[mail]
address=not_set@mail.com
period_size=7

[ban]
limit=50
nb_day=30

[network]
listen_port = 22
interface = 0.0.0.0
"""

SLOW_MILLISEC = 500
SQLITE_PATH = "logs.db"
EMAIL_ADDR = None
EMAIL_PERIOD = 7
BAN_LIMIT = 50
BAN_DAY_MAX = 30
NETWORK_TCP_PORT = 22
NETWORK_INTERFACE = ""


def load_config(filename=""):
    global SLOW_MILLISEC, SQLITE_PATH, EMAIL_ADDR, EMAIL_PERIOD, BAN_LIMIT, BAN_DAY_MAX, NETWORK_TCP_PORT

    config = configparser.ConfigParser()

    if filename == "":
        filename = os.path.expanduser(os.path.join("~", ".fake-ssh.ini"))

    # read the config filename
    config.read(filename)

    if "general" in config:
        if "slow_millisec" in config["general"]:
            SLOW_MILLISEC = int(config["general"]["slow_millisec"])
        if "sqlite_path" in config["general"]:
            SQLITE_PATH = config["general"]["sqlite_path"]
    if "mail" in config:
        if "address" in config["mail"]:
            EMAIL_ADDR = config["mail"]["address"]
        if "period" in config["mail"]:
            EMAIL_PERIOD = int(config["mail"]["period"])
    if "ban" in config:
        if "limit" in config["ban"]:
            BAN_LIMIT = int(config["ban"]["limit"])
        if "nb_day" in config["ban"]:
            BAN_DAY_MAX = int(config["ban"]["nb_day"])
    if "network" in config:
        if "listen_port" in config["network"]:
            NETWORK_TCP_PORT = int(config["network"]["listen_port"])

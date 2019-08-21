import os
import configparser


"""
example of INI file:

[general]
slow_millisec=INTEGER
sqlite_path=DATABASE_PATH

[mail]
address=EMAIL_ADDRESS
period_size=INTEGER

[ban]
limit=INTEGER
limit_period=INTEGER
nb_day=INTEGER

[network]
listen_port = INTEGER
interface = 0.0.0.0

[crypto]
key_type = rsa|dsa
key_size = 1024
"""

SLOW_MILLISEC = 500
SQLITE_PATH = "logs.db"
EMAIL_ADDR = None
EMAIL_PERIOD = 7
BAN_LIMIT = 50
BAN_LIMIT_PERIOD = 7
BAN_DAY_MAX = 30
NETWORK_TCP_PORT = 22
NETWORK_INTERFACE = ""
CRYPTO_KEY_TYPE = "rsa"
CRYPTO_KEY_SIZE = 1024


def load_config(filename=""):
    global SLOW_MILLISEC, SQLITE_PATH
    global EMAIL_ADDR, EMAIL_PERIOD
    global BAN_LIMIT, BAN_DAY_MAX, BAN_LIMIT_PERIOD
    global NETWORK_TCP_PORT, NETWORK_INTERFACE
    global CRYPTO_KEY_SIZE, CRYPTO_KEY_TYPE

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
        if "limit_period" in config["ban"]:
            BAN_LIMIT_PERIOD = int(config["ban"]["limit_period"])
        if "nb_day" in config["ban"]:
            BAN_DAY_MAX = int(config["ban"]["nb_day"])

    if "network" in config:
        if "listen_port" in config["network"]:
            NETWORK_TCP_PORT = int(config["network"]["listen_port"])
        if "interface" in config["network"]:
            NETWORK_INTERFACE = config["network"]["interface"]

    if "crypto" in config:
        if "key_type" in config["crypto"]:
            CRYPTO_KEY_TYPE = config["crypto"]["key_type"]
        if "key_size" in config["crypto"]["key_size"]:
            CRYPTO_KEY_SIZE = int(config["crypto"]["key_size"])

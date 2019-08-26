#!/usr/bin/env python3

import argparse
from fake_ssh.server import FakeSshServer
from fake_ssh import config
from fake_ssh import database


def _main():
    parser = argparse.ArgumentParser(description="Run the fake ssh server")
    parser.add_argument("-f", "--config", help="You can specify a custom configuration file", default="")
    args = parser.parse_args()

    config.load_config(args.config)
    database.init_db()

    srv = FakeSshServer()
    srv.start()


if __name__ == "__main__":
    _main()

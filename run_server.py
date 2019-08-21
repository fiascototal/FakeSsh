#!/usr/bin/env python3

import argparse
from fake_ssh.server import FakeSshServer


def _main():
    parser = argparse.ArgumentParser(description="Run the fake ssh server")
    parser.add_argument("-f", "--config", help="You can specify a custom configuration file", default="")
    args = parser.parse_args()

    srv = FakeSshServer(config_filename=args.config)
    srv.start()


if __name__ == "__main__":
    _main()

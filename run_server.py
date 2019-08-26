#!/usr/bin/env python3

import argparse
import time
from fake_ssh.server import FakeSshServer
from fake_ssh import config
from fake_ssh import database
from fake_ssh import schedule
from fake_ssh.mailer import send_mail


def _main():
    parser = argparse.ArgumentParser(description="Run the fake ssh server")
    parser.add_argument("-f", "--config", help="You can specify a custom configuration file", default="")
    args = parser.parse_args()

    config.load_config(args.config)
    database.init_db()

    schedule.do_every(send_mail, nb_days_period=config.EMAIL_PERIOD)

    srv = FakeSshServer()
    srv.start()

    while True:
        schedule.tick()
        time.sleep(1)


if __name__ == "__main__":
    _main()

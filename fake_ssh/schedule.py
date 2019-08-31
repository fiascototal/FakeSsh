"""
basic implementation of a timer that schedule threaded actions every X days
"""


import datetime
import threading
import logging

# global that contains the list of scheduled callbacks
_waiting_list = list()


def do_every(callback, nb_sec_period=0, nb_days_period=0):
    """ add a new callback and a period. It will run the callback every period """

    new_item = {
        "callback": callback,
        "period": datetime.timedelta(seconds=nb_sec_period, days=nb_days_period),
        "time_start": datetime.datetime.now(),
    }
    _waiting_list.append(new_item)


def tick():
    """ main function: check if we need to call the waiting list """

    now = datetime.datetime.now()
    for item in _waiting_list:
        if item["time_start"] + item["period"] < now:
            logging.info("run scheduler for %s" % str(item["callback"]))

            # call the callback
            t = threading.Thread(target=item["callback"])
            t.start()

            # reset the counter
            item["time_start"] = now

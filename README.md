FakeSsh
========

current version: v1.0

A fake ssh server (honeypot) that log every login requests.

Bored of every bots that try to connect to your SSH server ?
What if you can let them connect to a fake server and see what's append ?
For statistic purpose and for fun ^^!


Features
---------

* a mailer : send you some statistics about the number of connection attempts ...
* a login back : on each login request we try to log back to the bot using the same credentials.
    * If the connection succeeded we log the ip and credentials (sometime it works ^^) 
    * Don't know yet what to do with that ^^
    
Todo:
* check periodically if our list of working credentials still works
* improve the mailer to send better reports
* allow the connection and logs shells commands 


Installation
-------------

Requirements:
* Python 3.x
* some python dependencies
    * paramiko (for the SSH library)
    * peewee (for the database manipulation)
    
Works on Linux and Windows and more (it is a simple python script !)
    
Installation example for Linux, you will need to:
* install some packages: `$ sudo apt get install python3 python3-pip`
* install the python dependencies: `$ pip install -r requirements.txt`


Usage
------

Usage and help of the fake ssh server launcher:

```
$ ./run_server.py -h
usage: run_server.py [-h] [-f CONFIG]

Run the fake ssh server

optional arguments:
  -h, --help            show this help message and exit
  -f CONFIG, --config CONFIG
                        You can specify a custom configuration file
```

You will need to setup a configuration file. It is an INI file format and can be passed to the program using 2 different ways:
* default location is `~/.fake-ssh.ini`
* can be passed as an argument to the fake ssh server

Example of INI file:

```
[general]

# some millisec we wait between 2 attackers login tentatives
slow_millisec=INTEGER

# the path the the SQLite DB (connection logs will be saved in it)
sqlite_path=DATABASE_PATH

[mail]
# if you want to use the mailer to receive some statistics
address_from=EMAIL_ADDRESS
address_to=EMAIL_ADDRESS
smtp_host=HOST
smtp_port=INTEGER
smtp_login=USERNAME
smtp_password=PASSWORD
period_size=INTEGER

[ban]
# some limitation to block an attackant if he bruteforce too much
limit=INTEGER
limit_period=INTEGER
nb_day=INTEGER

[network]
listen_port = INTEGER
interface = 0.0.0.0

[crypto]
# for the SSH key generation (it generate a new key at the beginning)
key_type = rsa|dsa
key_size = 1024
```
import logging
import smtplib
import ssl
import datetime
import peewee
import os
from email.message import EmailMessage
from fake_ssh import config
from fake_ssh.database import DbIp, DbUsername, DbPassword, DbLog, DbBanned, DbValidAccount


def send_mail():
    if config.EMAIL_ADDR_FROM and config.EMAIL_ADDR_TO and config.EMAIL_SMTP_HOST:
        logging.info("[+] send mail")

        cur_date = datetime.datetime.now()
        first_date_log = DbLog.select().order_by(DbLog.id.asc()).get().date
        time_diff = cur_date - first_date_log
        period_diff = cur_date - datetime.timedelta(days=config.EMAIL_PERIOD)
        msg_content = """\
FAKE SSH SERVER - REPORT of %s
=================================================
        
TOTAL (%d days):
-----------------

* Number of IP addresses: %d
* Number of login: %d
* Number of passwords: %d
* Number of login requests: %d
* Number of banned accounts: %d
* Number of success login back: %d
* Top 10 password: %s
* Top 10 username: %s

LAST PERIOD (%d days)
----------------------

* Number of IP addresses: %d
* Number of login: %d
* Number of passwords: %d
* Number of login requests: %d
* Number of banned accounts: %d
* Number of success login back: %d

OTHER
-----

* database size: %d Ko
""" % (cur_date.strftime("%m/%d/%Y, %H:%M:%S"),
       time_diff.days,
       DbIp.select().count(),
       DbUsername.select().count(),
       DbPassword.select().count(),
       DbLog.select().count(),
       DbBanned.select().count(),
       DbValidAccount.select().count(),
       ", ".join([ "%s (x%d)" % (x.pwd, x.lol) for x in DbPassword.select(DbPassword.pwd, peewee.fn.COUNT(DbLog.password).alias("lol")).join(DbLog).group_by(DbLog.password).order_by(peewee.fn.COUNT(DbLog.password).desc()).limit(10)]),
       ", ".join(["%s (x%d)" % (x.name, x.lol) for x in
                  DbUsername.select(DbUsername.name, peewee.fn.COUNT(DbLog.username).alias("lol")).join(DbLog).group_by(
                      DbLog.username).order_by(peewee.fn.COUNT(DbLog.username).desc()).limit(10)]),
       config.EMAIL_PERIOD,
       DbIp.select().join(DbLog).where(DbLog.date > period_diff).group_by(DbLog.ip).count(),
       DbUsername.select().join(DbLog).where(DbLog.date > period_diff).group_by(DbLog.username).count(),
       DbPassword.select().join(DbLog).where(DbLog.date > period_diff).group_by(DbLog.password).count(),
       DbLog.select().where(DbLog.date > period_diff).count(),
       DbBanned.select().where(DbBanned.date > period_diff).count(),
       DbValidAccount.select().where(DbValidAccount.date_added > period_diff).count(),
       os.path.getsize(config.SQLITE_PATH) / 1024)

        msg = EmailMessage()
        msg.set_content(msg_content)
        msg['Subject'] = '[FAKE-SSH] periodic report'
        msg['From'] = config.EMAIL_ADDR_FROM
        msg['To'] = config.EMAIL_ADDR_TO

        try:
            # Create a secure SSL context
            context = ssl.create_default_context()

            server = smtplib.SMTP(config.EMAIL_SMTP_HOST, config.EMAIL_SMTP_PORT)
            server.ehlo()
            server.starttls(context=context)  # Secure the connection
            server.ehlo()

            if config.EMAIL_SMTP_USERNAME and config.EMAIL_SMTP_PASSWORD:
                server.login(config.EMAIL_SMTP_USERNAME, config.EMAIL_SMTP_PASSWORD)

            server.sendmail(config.EMAIL_ADDR_FROM, config.EMAIL_ADDR_TO, msg.as_bytes())
            server.close()

        except Exception as err:
            logging.error("[-] smtp failed: %s" % err)

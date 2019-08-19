import peewee
from fake-ssh import config


db = peewee.SqliteDatabase(config.SQLITE_PATH)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class DbIp(BaseModel):
    value = peewee.CharField(unique=True)


class DbUsername(BaseModel):
    name = peewee.CharField(unique=True)


class DbPassword(BaseModel):
    pwd = peewee.CharField(unique=True)


class DbLog(BaseModel):
    ip = peewee.ForeignKeyField(DbIp, backref="logs")
    username = peewee.ForeignKeyField(DbUsername, backref="logs")
    password = peewee.ForeignKeyField(DbPassword, backref="logs")
    date = peewee.DateTimeField()


class DbValidAccount(BaseModel):
    date_added = peewee.DateTimeField()
    date_last_check = peewee.DateTimeField()
    ip = peewee.ForeignKeyField(DbIp, backref="accounts")
    username = peewee.ForeignKeyField(DbUsername, backref="accounts")
    password = peewee.ForeignKeyField(DbPassword, backref="accounts")


class DbBanned(BaseModel):
    ip = peewee.ForeignKeyField(DbIp, backref="bans")
    date = peewee.DateTimeField()
    duration = peewee.IntegerField()


def connect():
    db.connect()


def create_tables():
    DbIp.create_table()
    DbUsername.create_table()
    DbPassword.create_table()
    DbLog.create_table()
    DbValidAccount.create_table()
    DbBanned.create_table()

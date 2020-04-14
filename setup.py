# This class is set-up your database configuration.
from loguru import logger

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cogs.utils.Database import Models
from cogs.utils.Database import MySQL
from configparser import *
auth = ConfigParser()
auth.read('auth.ini')

def main():
    DB_USER = auth.get("MySQL", "username")
    DB_PASS = auth.get("MySQL", "password")
    DB_HOST = auth.get("MySQL", "host")
    DB_DATABASE = auth.get("MySQL", "database")

    logger.info('Connecting to DB')
    Base = declarative_base()
    engine = MySQL.loadDB(DB_USER, DB_PASS, DB_HOST, DB_DATABASE)

    Models.DiscordGuild.__table__.create(engine, checkfirst=True)
    Models.WordBlackList.__table__.create(engine, checkfirst=True)
    Models.WordBanInfractions.__table__.create(engine, checkfirst=True)
    logger.success('Created tables')


if __name__ == '__main__':
    main()

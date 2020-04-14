from sqlalchemy import Column, String, Sequence, Integer, ForeignKey, BIGINT, TEXT, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class DiscordGuild(Base):
    __tablename__ = 'guild'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    guild_id = Column(Integer, unique=True)


class WordBlackList(Base):
    __tablename__ = 'word_black_list'
    id = Column(Integer, primary_key=True)
    guild_id = Column(BIGINT)
    banned_word = Column(String(30))

class WordBanInfractions(Base):
    __tablename__ = 'word_ban_infractions'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, default=datetime.datetime.utcnow)
    guild_id = Column(BIGINT)
    user_id = Column(BIGINT)
    message = Column(TEXT)

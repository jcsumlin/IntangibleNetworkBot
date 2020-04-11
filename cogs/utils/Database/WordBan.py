import discord
from loguru import logger
from sqlalchemy.orm import sessionmaker
from .MySQL import engine

from .Models import DiscordGuild, WordBlackList


class WordBan(object):
    def __init__(self, guild):
        self.engine = engine
        # Create a session
        Session = sessionmaker(bind=self.engine)
        self.guild = guild
        self.db = Session()


    async def add(self, word: str):
        check = self.db.query(DiscordGuild).filter_by(guild_id=self.guild.id).first()
        if check is None:
            new_server = WordBlackList(
                guild_id=self.guild.id,
                banned_word=word
            )
            self.db.add(new_server)
            self.db.commit()

    async def list(self):
        words = self.db.query(WordBlackList).filter_by(guild_id=self.guild.id).all()
        return words

    async def delete(self):
        pass

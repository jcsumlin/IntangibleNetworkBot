import discord
from loguru import logger
from sqlalchemy.orm import sessionmaker
from .MySQL import engine

from .Models import DiscordGuild, WordBlackList, WordBanInfractions


class WordBan(object):
    def __init__(self, guild):
        self.engine = engine
        # Create a session
        Session = sessionmaker(bind=self.engine)
        self.guild = guild
        self.db = Session()


    async def add(self, word: str):
        check = self.db.query(DiscordGuild).filter_by(guild_id=self.guild.id).one_or_none()
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

    async def delete(self, word):
        word_to_remove = self.db.query(WordBlackList).filter_by(guild_id=self.guild.id).filter_by(banned_word=word).one()
        word_to_remove.delete()

    async def add_infraction(self, message: discord.Message):
        new_infraction = WordBanInfractions(
            guild_id=self.guild.id,
            user_id=message.author.id,
            message=message.content
        )
        self.db.add(new_infraction)
        self.db.commit()

    async def get_infractions(self):
        infractions = self.db.query(WordBanInfractions).filter_by(guild_id=self.guild.id).all()
        formatted_infractions = []
        for infraction in infractions:
            user = discord.utils.find(lambda m: m.id == infraction.user_id, self.guild.members)
            if user is None:
                continue
            formatted_infraction = {
                "date_time": infraction.date_time,
                "user": discord.utils.find(lambda m: m.id == infraction.user_id, self.guild.members),
                "message": infraction.message
            }
            formatted_infractions.append(formatted_infraction)
        return formatted_infractions




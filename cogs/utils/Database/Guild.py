import discord
from loguru import logger
from sqlalchemy.orm import sessionmaker
from .MySQL import engine

from .Models import DiscordGuild, WordBlackList


class Database:
    def __init__(self, bot):
        self.bot = bot
        # Set-up the engine here.
        self.engine = engine
        # Create a session
        self.Session = sessionmaker(bind=self.engine)

    async def add_server_settings(self, guild: discord.Guild):
        check = self.engine.query(DiscordGuild).filter_by(server_id=guild.id).first()
        if check is None:
            new_server = DiscordGuild(
                guild_id=guild.id,
                name=guild.name
            )
            self.engine.add(new_server)
            self.engine.commit()

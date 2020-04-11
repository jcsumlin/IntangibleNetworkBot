import discord
from discord.ext import commands

from cogs.utils.checks import is_bot_owner_check

import git
from .utils.Database.WordBan import WordBan


class WordBlacklist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="wordban")
    async def wordban(self, ctx):
        pass

    @wordban.command(name="add")
    async def _add_banned_word(self, ctx, word):
        if len(word) > 30:
            raise discord.ext.commands.BadArgument
        try:
            wb = WordBan(ctx.guild)
            await wb.add(word)
        except Exception as e:
            return await ctx.send(f"{e}")
        await ctx.send(f"{word} was successfully added to the ban list")



def setup(bot):
    bot.add_cog(WordBlacklist(bot))

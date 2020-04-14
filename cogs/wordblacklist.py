import discord
from discord.ext import commands

from cogs.utils.checks import is_bot_owner_check
from .utils.chat_formatting import escape

import git
from .utils.Database.WordBan import WordBan


class WordBlacklist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="wordban")
    async def wordban(self, ctx):
        pass

    @wordban.command(name="delete")
    async def _list_banned_words(self, ctx, word):
        wb = WordBan(ctx.guild)
        if await wb.delete(word):
            await ctx.send(f"{word} was successfully removed from your list of banned words")

    @wordban.command(name="list")
    async def _list_banned_words(self, ctx):
        wb = WordBan(ctx.guild)
        w_list = await wb.list()
        embed = discord.Embed(
            title=f"List of banned words for {ctx.guild.name}",
            description=f"Use {ctx.prefix}wordban add [word] to add a word that is banned in your server",
            color=discord.Color.red()
        )
        embed.set_thumbnail(
            url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F99%2Fdd%2Fc5%2F99ddc5fa3cea296607ca06c132f2bee5.png&f=1&nofb=1")
        if len(w_list) > 0:
            list_of_banned_words = []
            for word in w_list:
                list_of_banned_words.append(word.banned_word)
            str_of_banned_words = ", ".join(list_of_banned_words)
            embed.add_field(name="Banned words", value=str_of_banned_words)
        else:
            embed.add_field(name="Banned words", value="None")
        await ctx.send(embed=embed)

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

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            wb = WordBan(message.guild)
            w_list = await wb.list()
            for word in w_list:
                if word.banned_word in message.content:
                    await message.delete()
                    embed = discord.Embed(
                        title=f":warning: Your message was deleted :warning:",
                        description=f"Your message \"**{message.content}**\" was "
                                    f"deleted because it contains content that is banned"
                                    f"on {message.guild.name}. The mods have been "
                                    f"notified of your infraction.",
                        color=discord.Color.red()
                    )
                    await wb.add_infraction(message)
                    await message.author.send(embed=embed)

    @wordban.command(name="infractions")
    async def _list_infractions(self, ctx):
        wb = WordBan(ctx.guild)
        infractions = await wb.get_infractions()
        embed = discord.Embed(
            title=f"Banned word infractions for {ctx.guild.name}",
            color=discord.Color.dark_orange()
        )
        embed.set_thumbnail(
            url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F99%2Fdd%2Fc5%2F99ddc5fa3cea296607ca06c132f2bee5.png&f=1&nofb=1"
        )
        for infraction in infractions:
            embed.add_field(
                name=f"Infraction by {escape(infraction['user'].name, formatting=True)}",
                value=f"**Message**: {infraction['message']}\n"
                      f"**Date & Time**: {infraction['date_time']} UTC")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(WordBlacklist(bot))

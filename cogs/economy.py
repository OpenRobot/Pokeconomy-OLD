import discord
from discord.ext import commands

class Economy(commands.Cog):

    async def test(self):
        pass


def setup(bot):
    bot.add_cog(Economy(bot))

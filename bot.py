import config
import discord
from discord.ext import commands
from discord.ext.commands.bot import when_mentioned_or
import asyncpg

intents = discord.Intents.all()
intents.guilds = True

bot = commands.Bot(
    command_prefix=when_mentioned_or("pc!", "pc?"),
    activity=discord.Activity(
        type=discord.ActivityType.playing,
        name="pc!help | a pokemon economy bot!"),
    slash_commands=True,
    intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")


@bot.command(aliases=["latency"])
async def ping(ctx):
    await ctx.reply(f"🏓Pong! `{round(bot.latency*1000)}ms`")

bot.pool = asyncpg.create_pool(config.database)

bot.load_extension("jishaku")

bot.run(config.token)
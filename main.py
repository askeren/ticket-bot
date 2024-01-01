import discord
from discord.ext import commands
from discord.commands import Option
import os
from dotenv import load_dotenv
import ezcord

intents = discord.Intents.default()
intents.members = True
status = discord.Status.online

bot = ezcord.Bot(
    intents=intents,
    status=status,
    debug_guilds=[]
)

@bot.event
async def on_ready():
    print(f"{bot.user} is online.")


if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    load_dotenv()
    bot.run(os.getenv("TOKEN"))

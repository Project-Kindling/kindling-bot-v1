import os
from dotenv import load_dotenv
import discord

load_dotenv()

bot = discord.Client()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('%'):
        print("Command given")

bot.run(os.environ['TOKEN'])
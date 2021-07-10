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
    if message.content.startswith('%hi'):
       await message.channel.send('hi <@' + str(message.author.id) + '>!')
    if message.content.startswith('%announce'):
        announcement = message.content[9:].strip()
        await channel.send(announcement)

bot.run(os.environ['TOKEN'])

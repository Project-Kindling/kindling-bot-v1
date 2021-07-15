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
        channel = bot.get_channel(863182926283014154) #channel id of receiving channel
        announcement = message.content[9:].strip()
        await channel.send(announcement)
    if message.content.startswith('%feedback'):
        channel=bot.get_channel(865314356798291969)
        feedback = message.content[9:].strip()
        anon_embed = discord.Embed(title="Anonymous Feedback", description=feedback, color=0xff3232)
        await channel.send(embed=anon_embed)

bot.run(os.environ['TOKEN'])

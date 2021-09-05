import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.utils import get
import datetime
from dataclasses import *

load_dotenv()

bot = commands.Bot(command_prefix='%')
bot.remove_command('help')

emotes = (
    "\U0001f1E6",
    "\U0001f1E7",
    "\U0001f1E8",
    "\U0001f1E9",
    "\U0001f1EA",
    "\U0001f1EB",
    "\U0001f1EC",
    "\U0001f1ED",
    "\U0001f1EE",
    "\U0001f1EF",
    "\U0001f1F0",
    "\U0001f1F1"
)

global len_of_options
len_of_options = 0
global auto_react
auto_react = 0

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='help')
async def helpcmd(ctx):
  embed = discord.Embed(title="Kindling Bot Commands", description="", colour=0x00ff00)
  embed.add_field(name="%feedback", value="Direct message Kindling Bot with this command to \
      anonymously send feedback to the Project Kindling moderators", inline=True)
  embed.add_field(name="%announce", value="Admin command that sends announcement content\
       to a designated announcement channel", inline=True)
  embed.add_field(name="%newpoll", value="Any user can create a poll with upto 12 options.\
  ```%newpoll \"The Poll\" a b c```", inline=True)
  await ctx.send(embed=embed)

@bot.command(name='feedback')
@commands.dm_only()
async def feedback(ctx):
  channel = bot.get_channel(865314356798291969)
  feedback_msg = ctx.message.content[9:].strip()
  embedvar = discord.Embed(title="Anonymous Feedback", description=feedback_msg, color=0xee6611)
  await channel.send(embed=embedvar)

@feedback.error
async def on_feedback_error(ctx, error):
  if isinstance(error, commands.PrivateMessageOnly):
    await ctx.send('This command can only be used in private messages.')
    await ctx.message.delete()

@bot.command(name='announce')
@commands.has_permissions(administrator=True)
async def announce(ctx):
  channel = bot.get_channel(863182926283014154) #channel id of receiving channel
  announcement = ctx.message.content[9:].strip()
  await channel.send(announcement)

@announce.error
async def on_announce_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('Only admins can run this command!')
    await ctx.message.delete()

@bot.command(name="newpoll")
async def new_poll(ctx, question, *options):
    global len_of_options
    len_of_options = len(options)
    if len(options) > 12:
        await ctx.send("You can have a maximum of 12 choices in your poll")

    else:
        embed = discord.Embed(title = "Poll",
                              description = question,
                              colour = discord.Colour.red())

        fields = [("Options", "\n".join([f"{emotes[idx]} {option}" for idx, option in enumerate(options)]), False),
                  ("Instructions", "Please react in order to vote!", False)]

        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline = inline)

        embed = embed.add_field(name = "Total votes", value = 0, inline = False)
        message = await ctx.send(embed = embed)

        for emoji in emotes[:len(options)]:
            await message.add_reaction(emoji)

        # message_win = await bot.get_channel(message.channel.id).fetch_message(message.id)
        # total_votes = sum(reaction.count for reaction in message_win.reactions) - len_of_options

        await message.edit(embed = embed)

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    global auto_react
    if auto_react < len_of_options:
        auto_react = auto_react + 1
        print(f"auto_react count is: {auto_react}")
    else:
        # tv_embed = message.embeds[0]
        total_votes = sum(reaction.count for reaction in message.reactions) - len_of_options
        print(f"Total votes: {total_votes}")
        print(f"Length of options: {len_of_options}")
        tv_embed = message.embeds[0].set_field_at(2, name = "Total votes", value = total_votes, inline = False)
        await message.edit(embed = tv_embed)

@bot.event
async def on_raw_reaction_remove(payload):
    print("Message removed")
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    total_votes = sum(reaction.count for reaction in message.reactions) - len_of_options
    print(f"Total votes: {total_votes}")
    print(f"Length of options: {len_of_options}")
    tv_embed = message.embeds[0].set_field_at(2, name = "Total votes", value = total_votes, inline = False)
    await message.edit(embed = tv_embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('%'):
        print("Command given")
    if message.content.startswith('%hi'):
        await message.channel.send('hi <@' + str(message.author.id) + '>!')
    await bot.process_commands(message)

bot.run(os.environ['TOKEN'])

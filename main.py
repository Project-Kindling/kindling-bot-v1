import os
from datetime import datetime
import re
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio

load_dotenv()

pytz.timezone('America/Toronto').localize(datetime.now())

bot = commands.Bot(command_prefix='%')
bot.remove_command('help')

sched = AsyncIOScheduler(timezone='America/Toronto')
#starting the scheduler
sched.start()

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
       ```%newpoll \"Quiz\" 1, 2, 3```", inline=True)
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
  if ctx.channel.id == 857375433812475922:

    msg_author = ctx.message.author
    role_id = discord.utils.get(ctx.guild.roles, name="Project Kindling Team")

    if role_id in msg_author.roles:

     await ctx.send("What would you like the title of your announcement to be? (type cancel anytime to end this process)")
     try:
       tit = await bot.wait_for("message", check=lambda m: m.author == ctx.author\
          and m.channel == ctx.channel, timeout=30.0)
     except: asyncio.TimeoutError
     else:
       if tit.content.lower() == "cancel":
         await ctx.send("Okay, cancelling")
         return
       else:
         await ctx.send("What would you like the content of your announcement to be?")
         try:
           con = await bot.wait_for("message", check=lambda m: m.author == ctx.author\
              and m.channel == ctx.channel, timeout=30.0)
         except: asyncio.TimeoutError
         else:
           if con.content.lower() == "cancel":
             await ctx.send("Okay, cancelling")
             return
           else:
             await ctx.send("What day and time would you like the announcement posted?\nUse this format: yyyy-mm-dd hh:mm:ss\nUse the 24hr clock format")
             try:
               timeof = await bot.wait_for("message", check=lambda m: m.author == ctx.author\
                  and m.channel == ctx.channel, timeout=30.0)
             except: asyncio.TimeoutError
             else:
               if timeof.content.lower() == "cancel":
                 await ctx.send("Okay, cancelling")
                 return
               else:
                 await ctx.send("Would you like to add an image to the announcement? (type yes/no)")
                 try:
                   sendimg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                 except: asyncio.TimeoutError
                 else:
                   if sendimg.content.lower() == "cancel":
                     await ctx.send("Okay, cancelling")
                     return
                   elif sendimg.content.lower() == "yes":
                     await ctx.send("Send your image")
                     try:
                       img = await bot.wait_for("message", check=lambda m: m.author == ctx.author and\
                          m.channel == ctx.channel, timeout=30.0)
                     except: asyncio.TimeoutError
                     else:
                       if img.content.lower() == "cancel":
                         await ctx.send("Okay, cancelling")
                         return
                       else:
                         await ctx.send("Your announcement will be sent on {}.\nHere is a preview".format(timeof.content))
                         embed = discord.Embed(title=tit.content,\
                           description=con.content, color=0xffe4e1)


                         embed.set_image(url=img.attachments[0].url)

                         await ctx.send(embed=embed)
                         await ctx.send("Type yes to confirm that you would like to send this announcement,\
                            type cancel and enter announce command again to restart the process")
                         try:
                           ans = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                         except: asyncio.TimeoutError
                         else:
                           if ans.content.lower() == "cancel":
                             await ctx.send("Okay, cancelling")
                             return
                           elif ans.content.lower() == "yes":
                             await ctx.send("Great!")
                             sched.add_job(anembed, 'date', run_date=timeof.content, args=[embed])
                   elif sendimg.content.lower() == "no":
                       await ctx.send("Your announcement will be sent on {}.\nHere is a preview".\
                       format(timeof.content))
                       embed = discord.Embed(title= tit.content,\
                         description=con.content, color=0xffe4e1)
                       await ctx.send(embed=embed)
                       await ctx.send("Type yes to confirm that you would like to send this announcement,\
                        type cancel and enter announce command again to restart the process")
                       try:
                         ans = await bot.wait_for("message", check=lambda m: m.author == ctx.author \
                         and m.channel == ctx.channel, timeout=30.0)
                       except: asyncio.TimeoutError
                       else:
                         if ans.content.lower() == "cancel":
                           await ctx.send("Okay, cancelling")
                           return
                         elif ans.content.lower() == "yes":
                           await ctx.send("Great!")
                           sched.add_job(anembed, 'date', run_date=timeof.content, args=[embed])
    else:
        msg_author_str = str(msg_author)
        to_rem_hashtag = msg_author_str.find("#")
        msg_wo_hashtag = msg_author_str[0:to_rem_hashtag]

        await ctx.send(f"Shoo! @{msg_wo_hashtag}, Shoo! You don't have the appropriate role!")
        await ctx.send(f"Sorry, you must have the role `{role_id}` to use this command.")
  else:
    await ctx.send("This command only works in the send announcements channel")

@announce.error
async def on_announce_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
      msg_author = ctx.message.author
      msg_author_str = str(msg_author)
      to_rem_hashtag = msg_author_str.find("#")
      msg_wo_hashtag = msg_author_str[0:to_rem_hashtag]

      await ctx.send(f"Shoo! @{msg_wo_hashtag}, Shoo! You don't have administrator permissions!")
      await ctx.message.delete()


async def anembed(embed):
  channel = bot.get_channel(863182926283014154)
 # allowed_mentions = discord.AllowedMentions(everyone = True, roles=True, users=True)
 # await channel.send(content = "@everyone", allowed_mentions = allowed_mentions)
  await channel.send(embed=embed)

@bot.command(name="newpoll")
@commands.has_permissions(administrator=True)
# @commands.has_role("Project Kindling Team")
async def newpoll(ctx):
    # role_check = ctx.message.guild.roles
    msg_author = ctx.message.author
    role_id = discord.utils.get(ctx.guild.roles, name="Project Kindling Team")
    print("role_id --- ", role_id)
    if role_id in msg_author.roles:
     msg_content = ctx.message.content[9:]
     print(f"msg_content --- {msg_content}")
     question = re.findall('"([^"]*)"', msg_content)
     question = ''.join(question)
     print(f"question type --- {type(question)}")
     print(f"question -- {question}")
     to_cut = len(question) + 2
     msg_options = msg_content[to_cut:]
     print(f"msg_options --- {msg_options}")
     raw_options = msg_options.split(',')
     raw_options = [r_op.strip() for r_op in msg_options.split(',')]
     print(f"raw_options --- {raw_options}")

     options = raw_options

     global len_of_options
     len_of_options = len(options)

     if len(options) > 12:
         await ctx.send("You can have a maximum of 12 choices in your poll")
     else:
         embed = discord.Embed(title="Poll",
                               description=question,
                               colour=discord.Colour.red())

         fields = [("Options", "\n".join([f"{emotes[idx]} {option}" for idx, option in enumerate(options)]), False),
                   ("Instructions", "Please react in order to vote!", False)]

         for name, value, inline in fields:
             embed.add_field(name=name, value=value, inline=inline)

         embed = embed.add_field(name="Total votes", value=0, inline=False)
         message = await ctx.send(embed=embed)

         for emoji in emotes[:len(options)]:
             await message.add_reaction(emoji)

         await message.edit(embed=embed)
    else:
        # msg_author = ctx.message.author
        msg_author_str = str(msg_author)
        to_rem_hashtag = msg_author_str.find("#")
        msg_wo_hashtag = msg_author_str[0:to_rem_hashtag]

        await ctx.send(f"Shoo! @{msg_wo_hashtag}, Shoo! You don't have the appropriate role!")
        await ctx.send(f"Sorry, you must have the role `{role_id}` to use this command.")

@bot.event
async def on_raw_reaction_add(payload):
    print("Message removed")
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    global auto_react
    if auto_react < len_of_options:
        auto_react = auto_react + 1
        print(f"auto_react count is: {auto_react}")
    else:
        # tv_embed = message.embeds[0]
        total_votes = sum(reaction.count for reaction in message.reactions) - len_of_options
        print(f"Total votes: {total_votes}")
        print(f"Length of options: {len_of_options}")
        tv_embed = message.embeds[0].set_field_at(2, name="Total votes", value=total_votes, inline=False)
        await message.edit(embed=tv_embed)

@bot.event
async def on_raw_reaction_remove(payload):
    print("Message removed")
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    total_votes = sum(reaction.count for reaction in message.reactions) - len_of_options
    print(f"Total votes: {total_votes}")
    print(f"Length of options: {len_of_options}")
    tv_embed = message.embeds[0].set_field_at(2, name="Total votes", value=total_votes, inline=False)
    await message.edit(embed=tv_embed)

@newpoll.error
async def on_newpoll_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
      msg_author = ctx.message.author
      msg_author_str = str(msg_author)
      to_rem_hashtag = msg_author_str.find("#")
      msg_wo_hashtag = msg_author_str[0:to_rem_hashtag]

      await ctx.send(f"Shoo! @{msg_wo_hashtag}, Shoo! You don't have administrator permissions!")
      await ctx.message.delete()

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

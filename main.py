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

emotes_alpha = (
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
emotes_num = (
    ":zero:",
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:",
    ":seven:",
    ":eight:"
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
#@commands.has_permissions(administrator=True)
async def announce(ctx):
  speciality_usr_li = [
   'Everyone',
   'Project Kindling Team & Campers',
   'STEM',
   'Architecture / Interior Design',
   'Law / Public Policy',
   'Arts / Design',
   'Business / Economics',
   'Politics / Political Science',
   'Other'
  ]
  speciality_tar_li = [
   '@everyone',
   '@Project Kindling Team @Campers',
   '@STEM',
   '@Architecture/Interior Design',
   '@Law/Public Policy',
   '@Arts/Design',
   '@Business/Economics',
   '@Politics/Political Science',
   '@Other'
  ]

  def gen_usr_face_li():
    show_speciality = [("Speciality", "\n".join([f"{emotes_num[idx]} {speciality_usr_li}" for idx, speciality_usr_li in enumerate(speciality_usr_li)]), False)]
    print(f"show_speciality ---> {show_speciality}")
    embed_speciality = discord.Embed(
      title="Choose Speciality of mentions",
      description="Please enter a which targets your announcement will ping.\nExample format: ` 3, 0, 5, 7 `",
      colour=discord.Colour.blue()
    )
    for name, value, inline in show_speciality:
      embed_speciality.add_field(name=name, value=value, inline=inline)
    return embed_speciality

  def match_uidx_to_lidx(uidx_int):
    check_set = {
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
    }
    arg_set = set(uidx_int)
    if arg_set.issubset(check_set):
      return True
    else:
      return False

  def uidx_to_int(usr_prov_idx):
    usr_prov_idx = usr_prov_idx.lower()
    try:
      uidx_int = [int(str_ele) for str_ele in usr_prov_idx.split(',')]
    except:
      if usr_prov_idx == "cancel":
        return "CANCEL"
      else:
        return "ERROR"
    check_bool = match_uidx_to_lidx(uidx_int)
    if check_bool == True:
      print(f"uidx_int ---> {uidx_int}")
      return uidx_int
    else:
      return "OUTOFSCOPE"

  def fetch_tar_ele(uidx_int):
    insert_idx = 0
    out_li = []
    for ele in uidx_int:
      if speciality_tar_li[ele] in out_li:
        pass
      else:
        out_li.append(speciality_tar_li[ele])
        insert_idx = insert_idx + 1
    print(out_li)
    out_str = '   '.join(out_li)
    print(f"out_str ---> {out_str}")
    return out_str

  if ctx.channel.id == 857375433812475922:

    msg_author = ctx.message.author
    role_id_1 = discord.utils.get(ctx.guild.roles, name="Project Kindling Team")
    role_id_2 = discord.utils.get(ctx.guild.roles, name="Moderator")
    if role_id_1 in msg_author.roles or role_id_2 in msg_author.roles:

     await ctx.send("What would you like the title of your announcement to be? (type cancel anytime to end this process)")
     try:
       tit = await bot.wait_for("message", check=lambda m: m.author == ctx.author\
          and m.channel == ctx.channel, timeout=1200.0)
     except: asyncio.TimeoutError
     else:
       if tit.content.lower() == "cancel":
         await ctx.send("Okay, cancelling")
         return
       else:
         await ctx.send("What would you like the content of your announcement to be?")
         try:
           con = await bot.wait_for("message", check=lambda m: m.author == ctx.author\
              and m.channel == ctx.channel, timeout=1200.0)
         except: asyncio.TimeoutError
         else:
           if con.content.lower() == "cancel":
             await ctx.send("Okay, cancelling")
             return
           else:
             await ctx.send(f"What day and time would you like the announcement posted?\nUse this format: `yyyy-mm-dd hh:mm:ss`\nUse the 24hr clock format")
             try:
               timeof = await bot.wait_for("message", check=lambda m: m.author == ctx.author\
                  and m.channel == ctx.channel, timeout=1200.0)
             except: asyncio.TimeoutError
             else:
               if timeof.content.lower() == "cancel":
                 await ctx.send("Okay, cancelling")
                 return
               else:
                 await ctx.send(f"Would you like to add an image to the announcement? `(yes/no)`")
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
                          m.channel == ctx.channel, timeout=90.0)
                     except: asyncio.TimeoutError
                     else:
                       if img.content.lower() == "cancel":
                         await ctx.send("Okay, cancelling")
                         return
                       else:
                         await ctx.send("Your announcement will be sent at this date and time: `{}`.\nHere is a preview".format(timeof.content))
                         embed = discord.Embed(title=tit.content,\
                           description=con.content, color=0xffe4e1)
                         embed.set_image(url=img.attachments[0].url)
                         await ctx.send(embed=embed)
                         try:
                           ans = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=60.0)
                         except: asyncio.TimeoutError
                         else:
                           if ans.content.lower() == "cancel":
                             await ctx.send("Okay, cancelling")
                             return
                           elif ans.content.lower() == "yes":
                             await ctx.send("Great!")
                             sched.add_job(anembed, 'date', run_date=timeof.content, args=[embed])
                   elif sendimg.content.lower() == "no":
                       await ctx.send("Your announcement will be sent at this date and time: `{}`.\nHere is a preview".\
                       format(timeof.content))
                       embed = discord.Embed(title= tit.content,\
                         description=con.content, color=0xffe4e1)
                       await ctx.send(embed=embed)
                       await ctx.send(f"Type `yes` to confirm that you would like to send this announcement.\ntype ` target ` if you want to choose, by specialty, who the announcements will ping, type `cancel` and enter\nthe `announce` command again to restart the process")
                       try:
                         ans = await bot.wait_for("message", check=lambda m: m.author == ctx.author \
                         and m.channel == ctx.channel, timeout=300.0)
                       except: asyncio.TimeoutError
                       else:
                         if ans.content.lower() == "cancel":
                           await ctx.send("Okay, cancelling")
                           return
                         elif ans.content.lower() == "yes":
                           await ctx.send("Great!")
                           sched.add_job(anembed, 'date', run_date=timeof.content, args=[embed])
                         elif ans.content.lower() == "target":
                           heartbeat = 1
                           while heartbeat == 1:
                             gen_usr_face_li()
                             await ctx.send(embed=gen_usr_face_li())
                             try:
                               ans = await bot.wait_for("message", check=lambda m: m.author == ctx.author \
                               and m.channel == ctx.channel, timeout=300.0)
                             except: asyncio.TimeoutError
                             else:
                               uidx_int = uidx_to_int(ans.content)
                               if uidx_int == "OUTOFSCOPE":
                                 await ctx.send("You are targetting a role that doesn't exist")
                                 await ctx.send("Please try again!")
                               elif uidx_int == "CANCEL":
                                 await ctx.send("Ok cancelling!")
                                 heartbeat = 0
                               elif uidx_int == "ERROR":
                                 await ctx.send("Please enter ` numbers ` not ` text `!")
                                 await ctx.send("Please try again!")
                               else:
                                 fetch_tar_ele(uidx_int)
                                 print("heartbeat ~IN LOOP~ ---> ", heartbeat)
                                 out_str = fetch_tar_ele(uidx_int)
                                 await ctx.send(f"The announcement will target the following roles:``` {out_str} ```\nType ` yes ` to confirm!\nType ` again ` to choose ping targets again!\nType ` cancel ` to cancel!")
                                 try:
                                   ans = await bot.wait_for("message", check=lambda m: m.author == ctx.author \
                                   and m.channel == ctx.channel, timeout=300.0)
                                 except: asyncio.TimeoutError
                                 else:
                                   if ans.content.lower() == 'cancel':
                                     await ctx.send("Ok cancelling!")
                                     heartbeat = 0
                                   elif ans.content.lower() == 'again':
                                     await ctx.send("Please choose again!")
                                   elif ans.content.lower() == 'yes':
                                       await ctx.send("Great!")
                                       sched.add_job(anembed, 'date', run_date=timeof.content, args=[embed, out_str])
                                       heartbeat = 0
                                   else:
                                     await ctx.send("Command not recognized!\nExiting")
                                     heartbeat = 0
                           print("heartbeat ~OUT OF LOOP~ ---> ",heartbeat)
    else:
        msg_author_str = str(msg_author)
        to_rem_hashtag = msg_author_str.find("#")
        msg_wo_hashtag = msg_author_str[0:to_rem_hashtag]

        await ctx.send(f"Shoo! @{msg_wo_hashtag}, Shoo! You don't have the appropriate role!")
        await ctx.send(f"Sorry, you must have either the `{role_id_1}` or `{role_id_2}` role to use this command.")
  else:
    await ctx.send("This command only works in the send announcements channel")

# @announce.error
# async def on_announce_error(ctx, error):
#   if isinstance(error, commands.MissingPermissions):
#       msg_author = ctx.message.author
#       msg_author_str = str(msg_author)
#       to_rem_hashtag = msg_author_str.find("#")
#       msg_wo_hashtag = msg_author_str[0:to_rem_hashtag]

#       await ctx.send(f"You don't have administrator permissions, @{msg_wo_hashtag}!")
#       await ctx.message.delete()


async def anembed(embed, out_str):
  channel = bot.get_channel(863182926283014154)
  allowed_mentions = discord.AllowedMentions(everyone = True, roles=True, users=True)
  # await channel.send(content = "<@&887727465382965268>", allowed_mentions = allowed_mentions)
  await channel.send(out_str)
  await channel.send(embed=embed)

@bot.command(name="newpoll")
# @commands.has_permissions(administrator=True)
# @commands.has_role("Project Kindling Team")
async def newpoll(ctx):
    msg_author = ctx.message.author
    role_id_1 = discord.utils.get(ctx.guild.roles, name="Project Kindling Team")
    role_id_2 = discord.utils.get(ctx.guild.roles, name="Moderator")
    # role_list = []
    # print("ROLES ---", discord.utils.get(ctx.guild.roles))
    # print(", ".join([str(r.id) for r in ctx.guild.roles]))
    # print(", ".join([str(r.name) for r in ctx.guild.roles]))

    print("role_id_1 ---> ", role_id_1)
    print("role_id_2 ---> ", role_id_2)
    if role_id_1 in msg_author.roles or role_id_2 in msg_author.roles:
     msg_content = ctx.message.content[9:]
     print(f"msg_content ---> {msg_content}")
     question = re.findall('"([^"]*)"', msg_content)
     question = ''.join(question)
     print(f"question type ---> {type(question)}")
     print(f"question ---> {question}")
     to_cut = len(question) + 2
     msg_options = msg_content[to_cut:]
     print(f"msg_options ---> {msg_options}")
     raw_options = msg_options.split(',')
     raw_options = [r_op.strip() for r_op in msg_options.split(',')]
     print(f"raw_options ---> {raw_options}")

     options = raw_options

     global len_of_options
     len_of_options = len(options)

     if len(options) > 12:
         await ctx.send("You can have a maximum of 12 choices in your poll")
     else:
         embed = discord.Embed(title="Poll",
                               description=question,
                               colour=discord.Colour.red())

         fields = [("Options", "\n".join([f"{emotes_alpha[idx]} {option}" for idx, option in enumerate(options)]), False),
                   ("Instructions", "Please react in order to vote!", False)]

         for name, value, inline in fields:
             embed.add_field(name=name, value=value, inline=inline)

         embed = embed.add_field(name="Total votes", value=0, inline=False)
         message = await ctx.send(embed=embed)

         for emoji in emotes_alpha[:len(options)]:
             await message.add_reaction(emoji)

         await message.edit(embed=embed)
    else:
        # msg_author = ctx.message.author
        msg_author_str = str(msg_author)
        to_rem_hashtag = msg_author_str.find("#")
        msg_wo_hashtag = msg_author_str[0:to_rem_hashtag]

        await ctx.send(f"Shoo! @{msg_wo_hashtag}, Shoo! You don't have the appropriate role!")
        await ctx.send(f"Sorry, you must have either the `{role_id_1}` or `{role_id_2}` role to use this command.")

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
    print(f"Total votes ---> {total_votes}")
    print(f"Length of options ---> {len_of_options}")
    tv_embed = message.embeds[0].set_field_at(2, name="Total votes", value=total_votes, inline=False)
    await message.edit(embed=tv_embed)

# @newpoll.error
# async def on_newpoll_error(ctx, error):
#   if isinstance(error, commands.MissingPermissions):
#       msg_author = ctx.message.author
#       msg_author_str = str(msg_author)
#       to_rem_hashtag = msg_author_str.find("#")
#       msg_wo_hashtag = msg_author_str[0:to_rem_hashtag]

#       await ctx.send(f"You don't have administrator permissions, @{msg_wo_hashtag}!")
#       await ctx.message.delete()

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
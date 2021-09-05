import os
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

pytz.timezone('America/Toronto').localize(datetime.now())

bot = commands.Bot(command_prefix='%')
bot.remove_command('help')

sched= AsyncIOScheduler(timezone='America/Toronto')
#starting the scheduler
sched.start()  

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

    await ctx.send("What would you like the title of your announcement to be? (type cancel anytime to end this process)")
    try:
      tit = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=30.0)
    except: asyncio.TimeoutError
    else:
      if tit.content.lower()=="cancel":
        await ctx.send("Okay, cancelling")
        return
      else:
        await ctx.send("What would you like the content of your announcement to be?")
        try:
          con = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=30.0)
        except: asyncio.TimeoutError
        else:
          if con.content.lower()=="cancel":
            await ctx.send("Okay, cancelling")
            return
          else:
            await ctx.send("What day and time would you like the announcement posted?\nUse this format: yyyy-mm-dd hh:mm:ss\nUse the 24hr clock format")
            try:
              timeof = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=30.0)
            except: asyncio.TimeoutError
            else:
              if timeof.content.lower()=="cancel":
                await ctx.send("Okay, cancelling")
                return
              else:
                await ctx.send("Would you like to add an image to the announcement? (type yes/no)")
                try:
                  sendimg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=30.0)
                except: asyncio.TimeoutError
                else:
                  if sendimg.content.lower()=="cancel":
                    await ctx.send("Okay, cancelling")
                    return
                  elif sendimg.content.lower()=="yes":
                    await ctx.send("Send your image")
                    try:
                      img = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=30.0)
                    except: asyncio.TimeoutError
                    else:
                      if img.content.lower()=="cancel":
                        await ctx.send("Okay, cancelling")
                        return
                      else:
                        await ctx.send("Your announcement will be sent on {}.\nHere is a preview".format(timeof.content))
                        embed=discord.Embed(title= tit.content,description=con.content, color=0xffe4e1)
                        

                        embed.set_image(url =img.attachments[0].url)

                        await ctx.send(embed=embed)
                        await ctx.send("Type yes to confirm that you would like to send this announcement, type cancel and enter announce command again to restart the process")
                        try:
                          ans = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=30.0)
                        except: asyncio.TimeoutError
                        else:
                          if ans.content.lower()=="cancel":
                            await ctx.send("Okay, cancelling")
                            return
                          elif ans.content.lower()=="yes":
                            
                            await ctx.send("Great!")
                            
                            sched.add_job(anembed,'date',run_date= timeof.content, args=[embed])
                            
                  elif sendimg.content.lower()=="no": 
                      await ctx.send("Your announcement will be sent on {}.\nHere is a preview".format(timeof.content))
                      embed=discord.Embed(title= tit.content,description=con.content, color=0xffe4e1)
                        
                      await ctx.send(embed=embed)
                      await ctx.send("Type yes to confirm that you would like to send this announcement, type cancel and enter announce command again to restart the process")
                      try:
                        ans = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=30.0)
                      except: asyncio.TimeoutError
                      else:
                        if ans.content.lower()=="cancel":
                          await ctx.send("Okay, cancelling")
                          return
                        elif ans.content.lower()=="yes":
                          await ctx.send("Great!")
                            
                          sched.add_job(anembed,'date',run_date= timeof.content, args=[embed])
                            
                        
                        
  else:
    await ctx.send("This command only works in the send announcements channel")
          

@announce.error
async def on_announce_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('Only admins can run this command!')
    await ctx.message.delete()


async def anembed(embed):
  channel=bot.get_channel(863182926283014154)
 # allowed_mentions = discord.AllowedMentions(everyone = True, roles=True, users=True)
 
 # await channel.send(content = "@everyone", allowed_mentions = allowed_mentions)
  await channel.send(embed=embed)

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

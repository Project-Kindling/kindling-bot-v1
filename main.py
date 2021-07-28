import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix='%')
bot.remove_command('help')

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
async def feedback(ctx, *, message):
  channel = bot.get_channel(865314356798291969)
  embedvar = discord.Embed(title="Anonymous Feedback", description=message, color=0xfe745a)
  await ctx.channel.send(embed=embedvar)

@feedback.error
async def on_feedback_error(ctx, error):
  if isinstance(error, commands.PrivateMessageOnly):
    await ctx.send('This command can only be sent through private messages.')
    await ctx.message.delete()

@bot.command(name='announce')
@commands.has_permissions(administrator=True)
async def announce(ctx, *, message):
  channel = bot.get_channel(863182926283014154) #channel id of receiving channel
  await channel.send(message)

@announce.error
async def on_announce_error(ctx,error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('Only admins can run this command!')
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

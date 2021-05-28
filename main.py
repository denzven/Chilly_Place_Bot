
import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
from coglist import cogs


defaults = os.listdir()
description = 'description'
intents = discord.Intents.all()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("="), intents = intents)



@bot.event
async def on_connect():
    print("the bot is ready")

@bot.event
async def on_ready():    
    print('We have logged in as {0.user}\n'.format(bot))
        
@bot.command()
async def ping(ctx):
    await ctx.send(f"ping ---> {round(bot.latency * 1000)} ms")
   

@bot.event
async def on_command(ctx):
    try:
        server = ctx.guild.name
        channel = ctx.channel
        user = ctx.author
        command = ctx.command
        print(f'{server} > {channel} > {user} > {command}')
    except Exception:
        return


@bot.event
async def on_ready():
    
    print('We have logged in as {0.user}\n'.format(bot))
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(f"{cog}")
        except Exception as e:
            print(e)
    for guild in bot.guilds:
        print(f'name:{guild.name}\nguild id:{guild.id}') 
    print('\n#######################')
    print('ready to rock and roll!')
    print('#######################')

@bot.command()
@commands.is_owner()
async def say(ctx, *,text:commands.clean_content):
    message = ctx.message
    await message.delete()
    await ctx.send(f"{text}")


@bot.event
async def on_command_error(ctx, error):
    raise error

keep_alive()
bot.run(os.environ['bottoken'])

import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
from coglist import cogs
from discord_components import DiscordComponents, Button, ButtonStyle
from asyncio import TimeoutError, sleep


defaults = os.listdir()
description = 'description'
intents = discord.Intents.all()
intents.members = True
intents.presences = True
#bot = commands.Bot(command_prefix=commands.when_mentioned_or("="))
bot = commands.Bot("=")
ddb = DiscordComponents(bot)

@bot.event
async def on_connect():
    print("the bot is ready")
        
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


import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle, InteractionType
import uuid

bot.poll_data = {}

@bot.command('poll')
async def poll(ctx, title, *names):
    poll_id = uuid.uuid4().hex

    data = []
    bot.poll_data[poll_id] = {
        'title': title,
        'items': {}
    }

    for i in names:
        item_id = uuid.uuid4().hex
        bot.poll_data[poll_id]['items'][f'{poll_id}.{item_id}'] = {
            'name': i,
            'users': []
        }
        data.append(Button(style=ButtonStyle.blue, label=i, id=f"{poll_id}.{item_id}"))
        components_data=data
    embed = discord.Embed(
        title=title,
        description="\n".join(map(lambda x: f'`{x}` : 0 votes', names)),
        color=0x58D68D
    )
    await ctx.send(embed=embed, components=[data])
    while True:
        res = await bot.wait_for("button_click")
        if res.channel == ctx.channel:
            full_id = res.component.id
            poll_id = full_id.split('.')[0]
            if not bot.poll_data.get(poll_id):
                return
            data = bot.poll_data[poll_id]
            user_id = res.user.id
            if user_id in data['items'][full_id]['users']:
                bot.poll_data[poll_id]['items'][full_id]['users'].remove(user_id)
            else:
                bot.poll_data[poll_id]['items'][full_id]['users'].append(user_id)
            embed = res.message.embeds[0]
            content = "\n".join(map(lambda x: f'`{data["items"][x]["name"]}` : {len(data["items"][x]["users"])} votes', data['items']))
            embed.description = content
            await res.respond(type=InteractionType.UpdateMessage, embed=embed, components=[components_data])






from ButtonPaginator import Paginator
from discord.ext.commands import Bot
from discord_components import DiscordComponents
import discord

@bot.command()
async def button(ctx):
    embeds = [discord.Embed(title="1 page"), discord.Embed(title="2 page"), discord.Embed(title="3 page"), discord.Embed(title="4 page"), discord.Embed(title="5 page")]
    e = Paginator(bot=bot,
                  ctx=ctx,
                  embeds=embeds,
                  only=ctx.author)
    await e.start()


import datetime
import discord
from discord.ext import commands
#from discord_slash import SlashCommand

#slash = SlashCommand(bot, sync_commands=True)
dc = DiscordComponents(bot)

buttons = [
    [
        Button(style=ButtonStyle.grey, label='1'),
        Button(style=ButtonStyle.grey, label='2'),
        Button(style=ButtonStyle.grey, label='3'),
        Button(style=ButtonStyle.blue, label='×'),
        Button(style=ButtonStyle.red, label='Exit')
    ],
    [
        Button(style=ButtonStyle.grey, label='4'),
        Button(style=ButtonStyle.grey, label='5'),
        Button(style=ButtonStyle.grey, label='6'),
        Button(style=ButtonStyle.blue, label='÷'),
        Button(style=ButtonStyle.red, label='←')
    ],
    [
        Button(style=ButtonStyle.grey, label='7'),
        Button(style=ButtonStyle.grey, label='8'),
        Button(style=ButtonStyle.grey, label='9'),
        Button(style=ButtonStyle.blue, label='+'),
        Button(style=ButtonStyle.red, label='Clear'),
    ],
    [
        Button(style=ButtonStyle.grey, label='00'),
        Button(style=ButtonStyle.grey, label='0'),
        Button(style=ButtonStyle.grey, label='.'),
        Button(style=ButtonStyle.blue, label='-'),
        Button(style=ButtonStyle.green, label='=')
    ],
    [
        Button(style=ButtonStyle.red, label='Shift')

    ],
]

buttons2 = [
    [
        Button(style=ButtonStyle.grey, label='sin'),
        Button(style=ButtonStyle.grey, label='cos'),
        Button(style=ButtonStyle.grey, label='tan'),
        Button(style=ButtonStyle.grey, label='deg'),
        Button(style=ButtonStyle.grey, label='rad')
    ],
    [
        Button(style=ButtonStyle.grey, label='cosec'),
        Button(style=ButtonStyle.grey, label='sec'),
        Button(style=ButtonStyle.grey, label='cot'),
        Button(style=ButtonStyle.grey, label='()'),
        Button(style=ButtonStyle.grey, label='^2')
    ],
    [
        Button(style=ButtonStyle.grey, label='√'),
        Button(style=ButtonStyle.grey, label='mod'),
        Button(style=ButtonStyle.grey, label='n!'),
        Button(style=ButtonStyle.grey, label='+'),
        Button(style=ButtonStyle.grey, label='Clear')
    ],
    [
        Button(style=ButtonStyle.grey, label='00'),
        Button(style=ButtonStyle.grey, label='0'),
        Button(style=ButtonStyle.grey, label='.'),
        Button(style=ButtonStyle.grey, label='-'),
        Button(style=ButtonStyle.green, label='=')
    ],
    [
        Button(style=ButtonStyle.red, label='Shift')

    ],
    
]

def calculate(exp):
    o = exp.replace('×','*')
    o = o.replace('÷','/')
    result=''
    try:
        result = str(eval(o))
    except:
        result='An error occurred.'
    return result


#@slash.subcommand(
#    base='utilities',
#   subcommand_group='calculators',
#    name='basic',
#    description='A simple calculator. Can\'t do anything too complex.'
#)
@bot.command()
async def calc(ctx):
    m = await ctx.send(content='Loading Calculators...')
    expression=' '
    delta = datetime.datetime.now()+ datetime.timedelta(minutes=5)
    #e = discord.Embed(title=f'{ctx.author.name}\'s calculator|{ctx.author.id}', description=f'```{expression}```',timestamp=delta)
    e = discord.Embed(title=f'{ctx.author.name}\'s calculator', description=f'```{expression}```')
    await m.edit(components=buttons, embed=e)
    print(f"{ctx.author.id} {ctx}")
    
    while m.created_at < delta:
        try:
            res = await bot.wait_for('button_click', timeout=20)
            print(f"{res.author.id} {ctx.author.id}")
            #if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[0].timestamp < delta:
            if int(res.author.id) == int(ctx.author.id):
                if expression==' ':
                    expression=' '
                if res.component.label == 'Exit':
                    await res.respond(content='Calculator Closed', type=7)
                    #break
                    return
                elif res.component.label == '←':
                    if expression == ' ':
                        expression = ' '
                    else:
                        expression=expression[:-1]
                elif res.component.label == 'Shift':
                    await m.edit(components=buttons2,embed = e)
                    print("hmmm")
                elif res.component.label == 'Clear':
                    expression=' '
                elif res.component.label == '=':
                    expression = calculate(expression)
                else:
                    expression+=res.component.label
                    print("hmmmmmmm")
            #e = discord.Embed(title=f'{ctx.author.name}\'s calculator|{ctx.author.id}', description=f'```{expression}```', timestamp=delta)
            e = discord.Embed(title=f'{ctx.author.name}\'s calculator', description=f'```{expression}```')
            await res.respond(content='',embed=e, components=buttons, type=InteractionType.UpdateMessage)
        except TimeoutError:
            await m.edit(content='Calculator Closed as noone responded',embed = e,components = [] ,type=7)
            print("time out")
            return

"""
      
@bot.command()
async def calculator(ctx):
    m = await ctx.send(content='Loading Calculators...')
    expression='None'
    delta = datetime.datetime.utcnow()+ datetime.timedelta(minutes=5)
    e = discord.Embed(title=f'{ctx.author.name}\'s calculator|{ctx.author.id}', description=expression, timestamp=delta)
    await m.edit(components=buttons, embed=e)
    while m.created_at < delta:
        res = await bot.wait_for('button_click')
        if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[0].timestamp < delta:
            expression = res.message.embeds[0].description
            if expression=='None' or expression == 'An error occurred.':
                expression=''
            if res.component.label == 'Exit':
                await res.respond(content='Calculator Closed', type=7)
                break
            elif res.component.label == '←':
                expression=expression[:-1]
            elif res.component.label == 'Clear':
                expression='None'
            elif res.component.label == '=':
                expression = calculate(expression)
            else:
                expression+=res.component.label
            f = discord.Embed(title=f'{res.author.name}\'s calculator|{res.author.id}', description=expression, timestamp=delta)
            await res.respond(content='',embed=f, components=buttons, type=7)
""" 
keep_alive()
bot.run(os.environ['bottoken'])
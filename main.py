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
bot = commands.Bot(command_prefix=commands.when_mentioned_or("="),
                   intents=discord.Intents.all(),
                   case_insensitive=True,
                   allowed_mentions=discord.discord.AllowedMentions.none())
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
async def say(ctx, *, text):
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
	bot.poll_data[poll_id] = {'title': title, 'items': {}}

	for i in names:
		item_id = uuid.uuid4().hex
		bot.poll_data[poll_id]['items'][f'{poll_id}.{item_id}'] = {
		    'name': i,
		    'users': []
		}
		data.append(
		    Button(style=ButtonStyle.blue, label=i, id=f"{poll_id}.{item_id}"))
		components_data = data
	embed = discord.Embed(title=title,
	                      description="\n".join(
	                          map(lambda x: f'`{x}` : 0 votes', names)),
	                      color=0x58D68D)
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
				bot.poll_data[poll_id]['items'][full_id]['users'].remove(
				    user_id)
			else:
				bot.poll_data[poll_id]['items'][full_id]['users'].append(
				    user_id)
			embed = res.message.embeds[0]
			content = "\n".join(
			    map(
			        lambda x:
			        f'`{data["items"][x]["name"]}` : {len(data["items"][x]["users"])} votes',
			        data['items']))
			embed.description = content
			await res.respond(type=InteractionType.UpdateMessage,
			                  embed=embed,
			                  components=[components_data])


from ButtonPaginator import Paginator
from discord.ext.commands import Bot
from discord_components import DiscordComponents
import discord


@bot.command()
async def button(ctx):
	embeds = [
	    discord.Embed(title="1 page"),
	    discord.Embed(title="2 page"),
	    discord.Embed(title="3 page"),
	    discord.Embed(title="4 page"),
	    discord.Embed(title="5 page")
	]
	e = Paginator(bot=bot, ctx=ctx, embeds=embeds, only=ctx.author)
	await e.start()


import datetime
import discord
from discord.ext import commands
from math import *
import math

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
    [Button(style=ButtonStyle.red, label='Shift')],
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
        Button(style=ButtonStyle.grey, label='('),
        Button(style=ButtonStyle.grey, label=')')
    ],
    [
        Button(style=ButtonStyle.grey, label='√'),
        Button(style=ButtonStyle.grey, label='mod'),
        Button(style=ButtonStyle.grey, label='n!'),
        Button(style=ButtonStyle.grey, label='x²'),
        Button(style=ButtonStyle.grey, label='Clear')
    ],
    [
        Button(style=ButtonStyle.grey, label='π'),
        Button(style=ButtonStyle.grey, label='0'),
        Button(style=ButtonStyle.grey, label='.'),
        Button(style=ButtonStyle.grey, label='-'),
        Button(style=ButtonStyle.green, label='=')
    ],
    [Button(style=ButtonStyle.red, label='shift')],
]


def calculate(exp):
	o = exp.replace('×', '*')
	o = o.replace('÷', '/')
	o = o.replace('²', '**2')
	o = o.replace('³', '**3')
	o = o.replace('!', str(math.factorial(4)))
	o = o.replace('π', str(math.pi))
	o = o.replace('√', 'sqrt')
	result = ''
	try:
		result = str(eval(o))
	except:
		result = 'An error occurred.'
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
	expression = ' '
	delta = datetime.datetime.now() + datetime.timedelta(minutes=5)
	#e = discord.Embed(title=f'{ctx.author.name}\'s calculator|{ctx.author.id}', description=f'```{expression}```',timestamp=delta)
	e = discord.Embed(
	    title=f'{ctx.author.name}\'s calculator⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
	    description=f'```{expression}```',
	    color=0x2f3136)
	current_btn = buttons
	await m.edit(components=current_btn, embed=e)

	while m.created_at < delta:
		try:
			res = await bot.wait_for('button_click', timeout=20)
			#if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[0].timestamp < delta:
			if int(res.author.id) == int(ctx.author.id):
				if expression == ' ':
					expression = ' '
				if res.component.label == 'Exit':
					await res.respond(content='Calculator Closed', type=7)
					#break
					return
				elif res.component.label == '←':
					if expression == ' ':
						expression = ' '
					else:
						expression = expression[:-1]
				elif res.component.label == 'Shift':
					current_btn = buttons2
				elif res.component.label == 'shift':
					current_btn = buttons
				elif res.component.label == 'Clear':
					expression = ' '
				elif res.component.label == '=':
					expression = calculate(expression)
				else:
					expression += res.component.label
			#e = discord.Embed(title=f'{ctx.author.name}\'s calculator|{ctx.author.id}', description=f'```{expression}```', timestamp=delta)
			e = discord.Embed(
			    title=f'{ctx.author.name}\'s calculator⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
			    description=f'```{expression}```',
			    color=0x2f3136)
			await res.respond(content='',
			                  embed=e,
			                  components=current_btn,
			                  type=InteractionType.UpdateMessage)
		except TimeoutError:
			await m.edit(content='Calculator Closed as noone responded',
			             embed=e,
			             components=[],
			             type=7)
			print("time out")
			return



import numpy as np
import matplotlib.pyplot as plt

async def f(x,a,b,c):
    return a*x**2+b*x+c

@bot.command()
async def graph(ctx,a:float,b:float,c:float):
    xlist = np.linspace(-10,10,num=1000)
    xlist2 = np.linspace(-10,10,num=10)

    ylist = a*xlist**2+b*xlist+c
    ylist2 = a*xlist2**2+b*xlist2+c

    #print(f"x={xlist}   y={ylist}")
    plt.figure(num=0,dpi=120)
    #ax = plt.gca()
    #ax.spines['top'].set_color('none')
    #ax.spines['left'].set_position('zero')
    #ax.spines['right'].set_color('none')
    #ax.spines['bottom'].set_position('zero')
    plt.scatter(xlist2,ylist2,s=30)
    plt.plot(xlist,ylist,label='parabola of the eqn')
    plt.legend()
    #plt.plot(xlist,ylist**(1/2),'--g',label=r"f(x)$^{0.5}$")
    plt.title(f"parabola of the equation {a}x²+{b}x+{c}")
    plt.grid(True)
    plt.savefig('plot.png',bbox_inches='tight', dpi=150)
    await ctx.send(file=discord.File('plot.png'))
    plt.close()
    return
    #plt.show()
    
@bot.command()
async def graph3d(ctx,randseed:int):
    np.random.seed(randseed)
    xs = np.random.random(100)
    ys = np.random.random(100)
    zs = np.random.random(100)
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs,ys,zs)
    #for ii in range(0,360,1):
        #ax.view_init(elev=10., azim=ii)
        #plt.savefig("renders/movie%d.png" % ii)
    plt.savefig('3dPlot.png',bbox_inches = 'tight',dpi = 150)
    await ctx.send(file=discord.File('3dPlot.png'))
    plt.close()
    return


@bot.command()
async def graph2(ctx,formula_og,tags=None):
    if formula_og.lower() == 'clear':
        plt.close()
        await ctx.send('cleared the graph')
    if tags == None:
        pass
    if tags == '-clear':
        plt.close()
        pass
    xlist = np.linspace(-10,10,num=1000)
    #ylist = np.linspace(-10,10,num=1000)
    #X, Y = np.meshgrid(xlist,ylist)
    formula = formula_og.replace('x','xlist')
    #formula = formula_og.replace('x','X')
    #formula = formula_og.replace('y','Y')
    formula = formula.replace('sin','np.sin')
    formula = formula.replace('cos','np.cos')
    formula = formula.replace('tan','np.tan')
    #F = formula
    print(f"{formula_og} {formula}" )
    ylist = eval(formula)
    #print(f"x={xlist}   y={ylist}")
    fig = plt.figure(num=0,dpi=120)
    #fig, ax = plt.subplots()
    #ax.contour(X,Y,F,[0])
    plt.plot(xlist,ylist,label=f'graph of {formula_og}')
    #plt.scatter(xlist,ylist)
    plt.legend()
    #plt.plot(xlist,ylist**(1/2),'--g',label=r"f(x)$^{0.5}$")
    plt.title(f"graphical representation of {formula_og}")
    plt.grid(True)
    if os.path.exists("plot2.png"):
        os.remove("plot2.png")
    else:
        print("The file does not exist")
    plt.savefig('plot2.png',bbox_inches='tight', dpi=150)
    await ctx.send(file=discord.File('plot2.png'))
    if tags == '-close':
        plt.close()
    return


@bot.command()
async def graph3(ctx,formula_og,tags=None):
    fig, ax = plt.subplots()
    #if formula_og.lower() == 'clear':
        #plt.close()
        #await ctx.send('cleared the graph')
    #if tags == 'hold':
        #pass
    #if tags == '-clear':
        #plt.close()
        #pass
    xlist = np.linspace(-10,10,num=1000)
    ylist = np.linspace(-10,10,num=1000)
    X, Y = np.meshgrid(xlist,ylist)
    
    formula = formula_og.replace('x','X')
    formula = formula.replace('y','Y')
    formula = formula.replace('sin','np.sin')
    formula = formula.replace('cos','np.cos')
    formula = formula.replace('tan','np.tan')
    formula = formula.replace('√','np.sqrt')
    formula = formula.replace('π','np.pi')
    
    chars = set('0123456789xy*/.-+()"√π×÷=^sinoctanp')
    char_check = ((c in chars) for c in formula_og)
    char_check_final =  all(char_check)
    if char_check_final:
        print('passable')
        pass
    else:
        print('nit passable')
        await ctx.send("no bish")
        return
        
    F = eval(formula)

    print(f"{formula_og} {formula}" )
    #fig, ax = plt.subplots(
    #plt.plot(xlist,ylist,label=f'graph of {formula_og}')
    #plt.scatter(xlist,ylist)
    #plt.legend()
    #plt.plot(xlist,ylist**(1/2),'--g',label=r"f(x)$^{0.5}$")
    ax.spines['bottom'].set_color('#787583')
    ax.spines['top'].set_color('#787583') 
    ax.spines['right'].set_color('#787583')
    ax.spines['left'].set_color('#787583')
    ax.tick_params(colors='white', which='both')
    ax.set_facecolor('#1d1925')
    fig.set_facecolor('#1d1925')

    ax.contour(X, Y, F, [0], colors = '#4c82ca', linestyles = 'solid')
    ax.set_aspect('equal')
    #plt.contour(X, Y, F, [0], linestyles = 'solid')
    #plt.set_aspect('equal')
    plt.title(f"graphical representation of {formula_og} = 0",color='w',pad = 20,fontsize = 'small')
    ax.grid(True)
    if os.path.exists("plot3.png"):
        os.remove("plot3.png")
    else:
        print("The file does not exist")
    fig.savefig('plot3.png',bbox_inches='tight', dpi=150)
    await ctx.send(file=discord.File('plot3.png'))
    #if tags == '-close':
        #plt.close()
    return








keep_alive()
bot.run(os.environ['bottoken'])

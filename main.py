
import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
from coglist import cogs
from dislash.slash_commands import *
from dislash.interactions import *
from discord_components import DiscordComponents, Button, ButtonStyle



defaults = os.listdir()
description = 'description'
intents = discord.Intents.all()
intents.members = True
intents.presences = True
#bot = commands.Bot(command_prefix=commands.when_mentioned_or("="))
bot = commands.Bot("=")
slash = SlashClient(bot)
ddb = DiscordComponents(bot)

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





from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


@bot.command()
async def test(ctx):
    # Make a row of buttons
    row_of_buttons = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="Green button",
            custom_id="green"
        ),
        Button(
            style=ButtonStyle.red,
            label="Red button",
            custom_id="red"
        )
    )
    # Send a message with buttons
    msg = await ctx.send(
        "This message has buttons!",
        components=[row_of_buttons]
    )
    # Wait for someone to click on them
    def check(inter):
        return inter.message.id == msg.id
    inter = await ctx.wait_for_button_click(check)
    # Send what you received
    button_text = inter.clicked_button.label
    await inter.reply(f"Button: {button_text}")





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

    embed = discord.Embed(
        title=title,
        description="\n".join(map(lambda x: f'`{x}` : 0 votes', names)),
        color=0x58D68D
    )
    embed.set_footer(text='Original Source: https://gist.github.com/minibox24/60acebe6322da42a16cc3822f2b747fe')
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

   
   
keep_alive()
bot.run(os.environ['bottoken'])
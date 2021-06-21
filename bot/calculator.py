import datetime
import discord
from discord.ext import commands
from discord.ext.commands import command, Cog
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

# from discord_slash import SlashCommand

# slash = SlashCommand(bot, sync_commands=True)


class calculator(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session_message = {}
        DiscordComponents(bot)

        buttons = [
            [
                Button(style=ButtonStyle.grey, label="1"),
                Button(style=ButtonStyle.grey, label="2"),
                Button(style=ButtonStyle.grey, label="3"),
                Button(style=ButtonStyle.blue, label="×"),
                Button(style=ButtonStyle.red, label="Exit"),
            ],
            [
                Button(style=ButtonStyle.grey, label="4"),
                Button(style=ButtonStyle.grey, label="5"),
                Button(style=ButtonStyle.grey, label="6"),
                Button(style=ButtonStyle.blue, label="÷"),
                Button(style=ButtonStyle.red, label="←"),
            ],
            [
                Button(style=ButtonStyle.grey, label="7"),
                Button(style=ButtonStyle.grey, label="8"),
                Button(style=ButtonStyle.grey, label="9"),
                Button(style=ButtonStyle.blue, label="+"),
                Button(style=ButtonStyle.red, label="Clear"),
            ],
            [
                Button(style=ButtonStyle.grey, label="00"),
                Button(style=ButtonStyle.grey, label="0"),
                Button(style=ButtonStyle.grey, label="."),
                Button(style=ButtonStyle.blue, label="-"),
                Button(style=ButtonStyle.green, label="="),
            ],
            [Button(style=ButtonStyle.red, label="Shift")],
        ]

        buttons2 = [
            [
                Button(style=ButtonStyle.grey, label="sin"),
                Button(style=ButtonStyle.grey, label="cos"),
                Button(style=ButtonStyle.grey, label="tan"),
                Button(style=ButtonStyle.grey, label="deg"),
                Button(style=ButtonStyle.grey, label="rad"),
            ],
            [
                Button(style=ButtonStyle.grey, label="cosec"),
                Button(style=ButtonStyle.grey, label="sec"),
                Button(style=ButtonStyle.grey, label="cot"),
                Button(style=ButtonStyle.grey, label="()"),
                Button(style=ButtonStyle.grey, label="^2"),
            ],
            [
                Button(style=ButtonStyle.grey, label="√"),
                Button(style=ButtonStyle.grey, label="mod"),
                Button(style=ButtonStyle.grey, label="n!"),
                Button(style=ButtonStyle.grey, label="+"),
                Button(style=ButtonStyle.grey, label="Clear"),
            ],
            [
                Button(style=ButtonStyle.grey, label="00"),
                Button(style=ButtonStyle.grey, label="0"),
                Button(style=ButtonStyle.grey, label="."),
                Button(style=ButtonStyle.grey, label="-"),
                Button(style=ButtonStyle.green, label="="),
            ],
            [Button(style=ButtonStyle.red, label="Shift")],
        ]

        def calculate(exp):
            o = exp.replace("×", "*")
            o = o.replace("÷", "/")
            result = ""
            try:
                result = str(eval(o))
            except:
                result = "An error occurred."
            return result

        # @slash.subcommand(
        #    base='utilities',
        #   subcommand_group='calculators',
        #    name='basic',
        #    description='A simple calculator. Can\'t do anything too complex.'
        # )

        @command()
        async def calc2(self, ctx):

            m = await ctx.send(content="Loading Calculators...")
            expression = " "

            delta = datetime.datetime.now() + datetime.timedelta(minutes=5)

            e = discord.Embed(
                title=f"{ctx.author.name}'s calculator|{ctx.author.id}",
                description=f"```{expression}```",
                timestamp=delta,
            )

            await m.edit(components=buttons, embed=e)

            # while m.created_at < delta:
            try:
                res = await self.bot.wait_for("button_click", timeout=20)
                print(f"{res.author.id} {ctx.author.id}")
                # if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[0].timestamp < delta:
                if int(res.author.id) == int(ctx.author.id):
                    if expression == " ":
                        expression = " "
                    if res.component.label == "Exit":
                        await res.respond(content="Calculator Closed", type=7)
                        # break
                        return
                    elif res.component.label == "←":
                        expression = expression[:-1]
                    elif res.component.label == "Shift":
                        await m.edit(components=buttons2, embed=e)
                        print("hmmm")
                    elif res.component.label == "Clear":
                        expression = " "
                    elif res.component.label == "=":
                        expression = calculate(expression)
                    else:
                        expression += res.component.label
                        print("hmmmmmmm")
                e = discord.Embed(
                    title=f"{ctx.author.name}'s calculator|{ctx.author.id}",
                    description=f"```{expression}```",
                    timestamp=delta,
                )
                await res.respond(
                    content="",
                    embed=e,
                    components=buttons,
                    type=InteractionType.UpdateMessage,
                )
            except TimeoutError:
                await m.delete()
                print("time out")
                # del session_message[ctx.author.id]
                return

        @command()
        async def cointoss(self, ctx):
            print("hmmm")


def setup(bot):
    bot.add_cog(calculator(bot))

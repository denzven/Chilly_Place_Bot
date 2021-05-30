import discord
import discord_components
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import random

class btns_are_pog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ddb = discord_components.DiscordComponents(self.bot)


    @commands.command(aliases=['coin'])
    async def flipcoin(self, ctx):
        '''Flips a coin'''
        choices = ['You got Heads', 'You got Tails']
        color = discord.Color.green()
        em = discord.Embed(color=color, title='Coinflip:', description=random.choice(choices))
        msg = await ctx.reply(
        embed=em,
        components=[
            Button(style=ButtonStyle.blue, label="Flip Again")])
        while True:
            res = await self.bot.wait_for("button_click")
            em2 = discord.Embed(color=color, title='Coinflip:', description=random.choice(choices))
            if res.channel == ctx.channel:
                await res.respond(
                  #type=InteractionType.ChannelMessageWithSource,
                  #type=InteractionType.UpdateMessage,
                  type = 7,
                  embed=em2
                )
                #await msg.edit(embed=em2, components=[Button(style=ButtonStyle.blue, label="Flip Again", disabled=False)])


def setup(bot):
    bot.add_cog(btns_are_pog(bot))

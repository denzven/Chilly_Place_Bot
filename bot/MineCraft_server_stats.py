from discord.ext import commands
from discord import utils
import discord

class Minecraft_serverstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: commands.clean_content):
        Minecraft_bot_id = 841144939407998996

        if message.author.id != Minecraft_bot_id:
            return

        if message.author.id == Minecraft_bot_id:
            if 'Type "/help" for help.' in message.content:
                minecraftChat_channel = self.bot.get_channel(841014501796085781)
                embed=discord.Embed(title="test", description="``` testy tests ```", color=0x04ff00)
                embed.add_field(name="Server IP:", value="`the_botboi.aternos.me`", inline=False)
                embed.set_footer(text="test it bishh")
                await  minecraftChat_channel.send(content="<@&841230563843113001> hehe ping pong",embed=embed)



            if "Server has started" in message.content:
                embed=discord.Embed(title="✅ The Server has Started ", description="``` the server is now ready to play! ```", color=0x00ff00)
                embed.add_field(name="Server IP:", value="`the_botboi.aternos.me`", inline=False)
                embed.set_footer(text="hope yall enjoy!")
                await  message.channel.send(content =  "the Server has Started! <@&841230563843113001>" ,embed=embed)



            if "Server has stopped" in message.content:
                embed=discord.Embed(title="🟥 The Server has Stoped ", description="``` hope yall had an awesome Time! ```", color=0xff0000)
                embed.add_field(name="Server IP:", value="`the_botboi.aternos.me`", inline=False)
                embed.set_footer(text="hope yall enjoyed!")
                await  message.channel.send(content =  "The Server has Stopped <@&841230563843113001>" ,embed=embed)

def setup(bot):
	bot.add_cog(Minecraft_serverstats(bot))
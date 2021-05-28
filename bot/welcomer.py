import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot=BaseException
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(member)
        guild = self.bot.get_guild(756596083458703530)
        channel = discord.utils.get(member.guild.channels, id=757894708147257374)   
        if channel is not None:
                await channel.send(f'sup {member.mention}, welcome to {guild.name} <:cp_hehe:843694680239767562> \n pingpong || <@$839742259020562433> ||')
        else:
            print("id channel wrong")

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        print(member)
        await member.send("hello")
        guild = self.bot.get_guild(756596083458703530)
        channel = discord.utils.get(member.guild.channels, id=757894708147257374) 
        if channel is not None:
                await channel.send(f'bye bye {member.mention} <:cp_heartburn:840479158412378113>  ')
        else:
            print("id channel wrong")

def setup(bot):
    bot.add_cog(Welcome(bot))
import asyncio
import contextlib

from discord import Embed, Forbidden, Message, NotFound, Role
from discord.embeds import _EmptyEmbed as EmptyEmbed
from discord.ext.commands import Cog
from discord.utils import get
import discord


class Bumprole(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener("on_message")
    async def disboard_bump(self, message: Message):
        disboard_bot_id = 302050872383242240
        supporter_role = 839421011292454913
        fake_supporter_role = 841013649568301116
        if message.guild == None:
            return
        if message.guild.id != 756596083458703530:
            return
        if message.author.id != disboard_bot_id:
            return
        if not message.embeds:
            return
        desc = message.embeds[0].description
        if isinstance(desc, EmptyEmbed):
            return

        if "Bump done" not in desc:
            # user_id_str = desc.split("\n")[0][2:-3]
            user_id_str = desc.split("\n")[0][2:20]
            user_id_str = user_id_str.replace("!d", "")
            user_id = int(user_id_str)
            guild = self.bot.get_guild(756596083458703530)
            user = guild.get_member(user_id)
            fake_supporter_role2 = get(guild.roles, id=fake_supporter_role)
            print(f"{user}{user_id} bumped {message.guild.name} unsuccessfully")
            embed = discord.Embed(
                title=f"Thank you for trying to bump the server i am proud of you {user}",
                description=f"you couldn't bump {guild.name} \n \n \n you are given {fake_supporter_role2.mention} for 5mins as a honour",
                color=0xFE7A7A,
            )
            embed.set_footer(text="thanks a ton for trying! 💜")
            channel = self.bot.get_channel(839368013232340992)
            print(channel)
            await channel.send(embed=embed)
            await user.add_roles(fake_supporter_role2)
            await asyncio.sleep(300)
            await user.remove_roles(fake_supporter_role2)
            return

        if "Bump done" in desc:
            user_id_str = desc.split("\n")[0][2:-3]
            # user_id_str = desc.split("\n")[0][2:20]
            user_id_str = user_id_str.replace("!d", "")
            user_id = int(user_id_str)
            guild = self.bot.get_guild(756596083458703530)
            user = guild.get_member(user_id)
            supporter_role2 = get(guild.roles, id=supporter_role)
            print(f"{user} bumped {message.guild.name} successfully")
            embed = discord.Embed(
                title=f"Thank you for bumping the server! {user.name}",
                description=f"you have successfully bumped {guild.name}",
                color=0x8DF782,
            )
            embed.add_field(
                name=f"new role and new places!!",
                value=f"you are awarded {supporter_role2.mention} for 2hrs!! check out all the new channels you've got acess!",
                inline=False,
            )
            embed.set_footer(text="thanks a ton! 💜")
            channel = self.bot.get_channel(839368013232340992)
            print(channel)
            await channel.send(embed=embed)
            print(f"{user} bumped {message.guild.name} successfully")
            await user.add_roles(supporter_role2)
            await asyncio.sleep(7200)
            await user.remove_roles(supporter_role2)
            return


def setup(bot):
    bot.add_cog(Bumprole(bot))

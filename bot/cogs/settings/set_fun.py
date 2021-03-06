import discord
from discord.ext import commands
from typing import Optional

from utils import util_settings

class SetFun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """This cog is for server admins only"""
        return ctx.author.guild_permissions.administrator
        
    @commands.command(
        name="setpingroulettechannel", 
        aliases=["sprc"],
        brief="Sets ping roulette message channel",
        help="Sets the channel for ping roulette messages. If no channel set, the roulette will ping people in the same channel the command was used.",
    )
    async def setpingroulettechannel(
        self, ctx, channel: discord.TextChannel=None
    ):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            ping_roulette_channel=channel.id if channel else None,
        )
        
    @commands.command(
        name="setbirthdayfeedchannel", 
        aliases=["sbfc", "sbdfc"],
        brief="Sets birthday feed channel",
        help="Sets the channel for birthday notification messages",
    )
    async def setbirthdayfeedchannel(
        self, ctx, channel: discord.TextChannel=None
    ):
        await util_settings.change_guild_setting(
            self.bot, 
            guild_id=ctx.guild.id,
            birthday_feed_channel_id=channel.id if channel else None,
        )
        

def setup(bot):
    bot.add_cog(SetFun(bot))
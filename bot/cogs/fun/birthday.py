"""This cog is for automatically announcing members' birthdays"""

import discord
from discord.ext import commands, tasks
from random import seed, choice
from datetime import datetime
from asyncio import sleep

from utils import util_fun
        
class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_feed.start()
        self.titles = [   
            "🍰 Happy Birthday! 🍰",
            "🧁 Happy Birthday! 🧁",
            "🎂 Happy Birthday! 🎂",
            "🎊 Happy Birthday! 🎊",
            "🎉 Happy Birthday! 🎉",
        ]
        self.cakes = [  # Yes, I host images on my wordpress website
            "https://apocake.files.wordpress.com/2020/01/cake-1.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-2.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-3.jpg",  # Pizza cake
            "https://apocake.files.wordpress.com/2020/01/cake-4.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-5.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-6.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-7.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-8.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-9.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-10.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-11.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-12.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-13.jpg",  # Swastika cake
            "https://apocake.files.wordpress.com/2020/01/cake-14.jpg",  # Rude cake
            "https://apocake.files.wordpress.com/2020/01/cake-15.png",  # Sushi cake
            "https://apocake.files.wordpress.com/2020/01/cake-16.jpg",  # Raw chicken cake
            "https://apocake.files.wordpress.com/2020/01/cake-17.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-18.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-19.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-20.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-21.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-22.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-23.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-24.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-25.jpg",
            "https://apocake.files.wordpress.com/2020/01/cake-26.jpg",  # Hercules beetle maggot cake
            "https://apocake.files.wordpress.com/2020/07/cake-27.jpg",
            "https://apocake.files.wordpress.com/2020/07/cake-28.jpg",
            "https://apocake.files.wordpress.com/2020/07/cake-29.jpg",
            "https://apocake.files.wordpress.com/2020/07/cake-30.jpg",
            "https://apocake.files.wordpress.com/2020/07/cake-31.jpg",  # Engineer cake
            "https://apocake.files.wordpress.com/2020/07/cake-32.jpg",
            "https://apocake.files.wordpress.com/2020/07/cake-33.jpg",  # Protests cake
            "https://apocake.files.wordpress.com/2020/07/cake-34.jpg",  # Shrek cake
            "https://apocake.files.wordpress.com/2020/07/cake-35.jpg",
            "https://apocake.files.wordpress.com/2020/07/cake-36.jpg",
        ]
        self.colors = [
            discord.Color(i) for i in (
                0xff7f7f, 0xffbf80, 0xffff80, 0xbfff80, 0x80ff80, 0x80ffbf,
                0x80ffff, 0x80bfff, 0x8080ff, 0xbf80ff, 0xff80ff, 0xff80bf,
            )
        ]

    def cog_unload(self):
        self.birthday_feed.cancel()
        
    @tasks.loop(hours=24)
    async def birthday_feed(self):
        seed()
        born_today = await util_fun.fetch_born_today(self.bot)
        for guild, settings in self.bot.settings.items():
            birthday_feed = settings.get("birthday_feed_channel_id")
            if birthday_feed:
                guild = self.bot.get_guild(guild)
                birthday_feed = guild.get_channel(birthday_feed)
                guild_birthdays = [
                    f"{m.mention} ({m.display_name})" 
                    for m in guild.members if m.id in born_today
                ]
                if guild_birthdays:
                    guild_birthdays = '\n'.join(guild_birthdays)
                    embed = discord.Embed(
                        title=choice(self.titles),
                        description=f"Congratulations to:\n\n{guild_birthdays}",
                        color=choice(self.colors),
                    )
                    embed.set_image(url=choice(self.cakes))
                    await birthday_feed.send(embed=embed)
                    
    @birthday_feed.before_loop
    async def before_birthday_feed(self):
        """Wait for 10:00"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure the bot reads settings
        difference = datetime.now() - datetime.now().replace(
            hour=10, minute=0, second=0, microsecond=0
        )
        await sleep(abs(difference).total_seconds())
    
def setup(bot):
    bot.add_cog(Birthdays(bot))
"""Automated server staff votes"""

from datetime import datetime, timedelta
from asyncio import sleep
from re import sub

import discord
from discord.ext import tasks, commands

from utils import util_users, util_user_stats, utils


class Votes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.numbers = [
            ':1icon:658633333051228161', ':2icon:658633333692956673',':3icon:658633334255124480', ':4icon:658633333625847809',':5icon:658633333877637130', ':6icon:658633334217244682',':7icon:658633334288678922', ':8icon:658633334234152980',':9icon:658633334234021898', 
            ':10icon:658633333919711235',':11icon:658633333395423242', ':12icon:658633334158524417',':13icon:658633334028763137', ':14icon:658633333688893444',':15icon:658633334171238410', ':16icon:658633334049734677',':17icon:658633333688893464', ':18icon:658633334141747200',':19icon:658633334183821322', 
            ':20icon:658633334338879518',':21icon:658633334192341022', ':22icon:658633333911322624',':23icon:658633334036889613', ':24icon:658633334167175179',':25icon:658633334250930189', ':26icon:658633334234152981',':27icon:658633334556983317', ':28icon:658633334704046080', ':29icon:658633334263644161', 
            ':30icon:658633334548725780', ':31icon:658633334456451082', ':32icon:658633334418702357', ':33icon:658633334284484619', ':34icon:658633334540468244', ':35icon:658633334695395351', ':36icon:658633334506913806', ':37icon:658633334473228288', ':38icon:658633334208856085', ':39icon:658633334347268137', 
            ':40icon:658633334368370700', ':41icon:658633334439542785', ':42icon:658633334490136587',':43icon:658633334473359370', ':44icon:658633334527623168',':45icon:658633334548856844', ':46icon:658633334489874462',':47icon:658633334527754260', ':48icon:658633334787932180',':49icon:658633334422896651', ':50icon:658633334288678913',
        ]
        self.votes.start()

    def cog_unload(self):
        self.votes.cancel()

    @commands.Cog.listener() 
    async def on_raw_reaction_add(self, payload):
        # If ??????, vote period and the voter has at least the active member role
        if str(payload.emoji) != "??????":
            return
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        voter = guild.get_member(payload.user_id)
        settings = self.bot.settings.get(guild.id)
        if message.embeds and \
            "Junior mod vote start" not in message.embeds[0].title or \
            message.author != guild.me or voter.bot:
            return
        now = datetime.now()
        junior_mod_vote_day = settings.get("vote_junior_mod_day")
        junior_mod_vote_months = settings.get("vote_junior_mod_months")
        senior_mod_vote_day = settings.get("vote_senior_mod_day")
        senior_mod_vote_months = settings.get("vote_senior_mod_months")
        admin_vote_day = settings.get("vote_admin_day")
        admin_vote_months = settings.get("vote_admin_months")
        if not any((
            junior_mod_vote_day and junior_mod_vote_months and \
            junior_mod_vote_day <= now.day <= junior_mod_vote_day + 5 and \
            now.month in junior_mod_vote_months,
            senior_mod_vote_day and senior_mod_vote_months and \
            senior_mod_vote_day <= now.day <= senior_mod_vote_day + 5 and \
            now.month in senior_mod_vote_months,
            admin_vote_day and admin_vote_months and \
            admin_vote_day <= now.day <= admin_vote_day + 5 and \
            now.month in admin_vote_months,
        )):
            await message.remove_reaction('??????', voter)
            #return
        active_member = guild.get_role(settings.get("rank_active_member_role_id"))
        junior_mod = guild.get_role(settings.get("rank_junior_mod_role_id"))
        senior_mod = guild.get_role(settings.get("rank_senior_mod_role_id"))
        if active_member not in voter.roles and \
            junior_mod not in voter.roles and \
            senior_mod not in voter.roles:
            await message.remove_reaction('??????', voter)
            #return
        # Fetch the candidate list from the vote start message
        raw_candidates = message.embeds[0].description.split("\n")[1:]
        raw_candidates = [i.split("<")[1] for i in raw_candidates]
        candidates = []
        for m in raw_candidates:
            m_id = sub("[^0-9]", "", m)
            m = guild.get_member(m_id) 
            if not m: m = await self.bot.fetch_user(m_id)
            candidates.append(m)
        # Build new embed(s) and send it(them) to the voter
        for num, candidate in enumerate(candidates):
            candidates[num] = f"<{self.numbers[num]}> {candidate.display_name} {candidate.mention}"
        desc_embed = discord.Embed(
            title=message.embeds[0].title.replace("start ", "") + " on " + guild.name,
            color=guild.me.color
        )
        desc_embed.description = f"React to the messages below with candidate numbers to vote for them.\n\n**Important** - If you're among the candidates, but don't want the promotion - don't upvote yourself. If the embed misses some reactions, rereact to the initial [vote message]({message.jump_url}) on server."
        embeds = []
        for i in range(len(candidates)//20 + int(len(candidates)%20 != 0)):
            embed = discord.Embed(
                title=message.embeds[0].title.replace("start ", "") + " on " + guild.name + " candidates",
                description="\n".join(candidates[i*20:(i+1)*20]),
                color=guild.me.color
            )
            embeds.append(embed)
        # Sending embeds and adding reactions to them
        await voter.send(embed=desc_embed)
        for num, embed in enumerate(embeds):
            msg = await voter.send(embed=embed)
            for number in range(num*20, min((num+1)*20, len(candidates))):
                await msg.add_reaction(self.numbers[number])
        
    @tasks.loop(hours=24.0)
    async def votes(self):
        """Run the votes for server staff"""
        for guild, settings in self.bot.settings.items():
            now = datetime.now()
            guild = self.bot.get_guild(guild)
            vote_channel = guild.get_channel(settings.get("vote_channel_id"))
            if not vote_channel: continue

            active_member = guild.get_role(settings.get("rank_active_member_role_id"))
            junior_mod = guild.get_role(settings.get("rank_junior_mod_role_id"))
            senior_mod = guild.get_role(settings.get("rank_senior_mod_role_id"))
            admin = guild.get_role(settings.get("rank_admin_role_id"))
            # Determine which votes trigger

            # JM vote
            junior_mod_vote_day = settings.get("vote_junior_mod_day")
            junior_mod_vote_months = settings.get("vote_junior_mod_months")
            junior_mod_vote_limit = settings.get("vote_junior_mod_limit")
            if junior_mod_vote_day and junior_mod_vote_months and \
                now.day == junior_mod_vote_day and \
                now.month in junior_mod_vote_months:
                
                junior_mod_days = settings.get("rank_junior_mod_required_days")
                junior_mod_activity = settings.get("rank_junior_mod_required_activity")
                # Find eligible members    
                members = await util_users.fetch_users_by_days_and_activity(
                    self.bot, guild, junior_mod_days, junior_mod_activity
                )
                members = [
                    m for m in members 
                    if senior_mod not in m.roles
                    and admin not in m.roles
                ]
                activities = [
                    int(await util_user_stats.fetch_average_activity(
                        self.bot, guild.id, m.id, days_back=60
                    )) for m in members
                ]
                table = zip(activities, [f"`{m.mention}" for m in members])
                table = list(zip(*sorted(table, key=lambda t: -t[0])))
                table[0] = [f"`{i}" for i in table[0]]
                table = utils.format_columns(
                    table, 
                    headers=("`ACTIVITY", "MEMBER`")
                )
                # Post a list of them to the vote channel
                e = discord.Embed(
                    title=f"Junior mod vote start {now.year}/{now.month}",
                    description=table,
                    color=guild.me.color
                )
                e.add_field(
                    name="Terms",
                    value=(
                        "The vote is anonymous. React to this message with ?????? to receive your form.\n"
                        f"To be eligible, candidates must earn {junior_mod_activity} average daily activity in the last {junior_mod_days} days.\n"
                        "It's possible to get promoted, demoted or keep your current rank.\n"
                        "Make sure to vote for yourself if you want to get promoted.\n"
                        "Only members with at least 25% of max possible upvotes get promoted.\n"
                        f"The max number of {junior_mod.mention} that can be vote-picked is {junior_mod_vote_limit}.\n"
                        f"Only members with {active_member.mention} or higher role can vote here.\n"
                        "The vote results will be published in 5 days."
                    )
                )
                vote_msg = await vote_channel.send(embed=e)
                await vote_msg.add_reaction("??????")
                # DM eligible voters the bulletins
            elif junior_mod_vote_day and junior_mod_vote_months and \
                now.day == junior_mod_vote_day + 5 and \
                now.month in junior_mod_vote_months:
                print("Junior mod vote end!")
                # Count the votes
                # Declare the results and implement them
            
            # SM vote
            senior_mod_vote_day = settings.get("vote_senior_mod_day")
            senior_mod_vote_months = settings.get("vote_senior_mod_months")
            if senior_mod_vote_day and senior_mod_vote_months and \
                now.day == senior_mod_vote_day and \
                now.month in senior_mod_vote_months:
                print("Senior mod vote start!")
                # Find eligible members    
                # Post a list of them to the vote channel
                # DM eligible voters the bulletins
            elif senior_mod_vote_day and senior_mod_vote_months and \
                now.day == senior_mod_vote_day + 5 and \
                now.month in senior_mod_vote_months:
                print("Senior mod vote end!")
                # Count the votes
                # Declare the results and implement them
            
            # A vote
            admin_vote_day = settings.get("vote_admin_day")
            admin_vote_months = settings.get("vote_admin_months")
            if admin_vote_day and admin_vote_months and \
                now.day == admin_vote_day and \
                now.month in admin_vote_months:
                print("Admin vote start!")
                # Find eligible members    
                # Post a list of them to the vote channel
                # DM eligible voters the bulletins
            elif admin_vote_day and admin_vote_months and \
                now.day == admin_vote_day + 5 and \
                now.month in admin_vote_months:
                print("Admin vote end!")
                # Count the votes
                # Declare the results and implement them
    
    # Enable this when the cog is functional
    '''@votes.before_loop
    async def before_votes(self):
        """Sleeping until the given time"""
        await self.bot.wait_until_ready()
        await sleep(5) # To make sure bot reads settings
        now = datetime.now()
        next_day = now.replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        await sleep((next_day - now).total_seconds())'''


def setup(bot):
    bot.add_cog(Votes(bot))

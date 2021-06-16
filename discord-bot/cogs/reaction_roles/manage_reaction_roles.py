"""Reaction roles creation and editing"""

import typing
import re
from asyncio import TimeoutError

import discord
from discord.ext import commands

from utils import output, reaction_roles, parsers

re_url_pattern = r"([0-9]+)\/([0-9]+)\/([0-9]+)"
new_rr = discord.Embed(
    title="Reaction roles",
    description="Click on the reactions below to get the roles",
)

async def add_reaction_role(bot, ctx, input_message, rr_message):
    emote, role = await parsers.parse_reaction_role_pair(input_message.content, ctx)
    res = await reaction_roles.add_reaction_role(
        bot, ctx.author.id, emote, role.id, rr_message.id,
    )
    print(res.__dict__) # TODO work with res

    if rr_message.author == ctx.guild.me:
        new_embed = rr_message.embeds[0] if rr_message.embeds else new_rr
        roles_field = -1
        for num, field in enumerate(new_embed.fields):
            if field.name.lower() == "roles":
                roles_field = num
                value = field.value + f"\n{emote} {role.mention}"
                new_embed.set_field_at(roles_field, name="Roles", value=value)
        if roles_field == -1:
            new_embed.add_field(name="Roles", value=f"{emote} {role.mention}")
        await rr_message.edit(embed=new_embed)
        await rr_message.add_reaction(emote)


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="reactionroles", 
        aliases=["rr"],
        help="Command group for managing reaction roles",
        invoke_without_command=True
    )
    async def manage_reaction_roles(self, ctx):
        await respond(ctx, "Reaction roles root!") # TODO return help
        
    @manage_reaction_roles.command(
        name="new", 
        aliases=["n"],
        help="Creates new reaction roles message. You can specify a channel to send a new message or provide a message link. The bot will edit its own reaction roles message with the roles it assigns.", 
    )
    async def new_reaction_roles(self, ctx, message_url: typing.Union[discord.TextChannel, str]):
        if isinstance(message_url, discord.TextChannel):
            message = await message_url.send(embed=new_rr)
            res = await reaction_roles.new_reaction_roles(
                self.bot, ctx.author.id, ctx.guild.id, message_url.id, message.id
            )
        else:
            m = re.search(re_url_pattern, message_url)
            if m is None:
                raise ValueError("Invalid message URL")
            guild = self.bot.get_guild(int(m.group(1)))
            channel = guild.get_channel(int(m.group(2)))
            message = await channel.fetch_message(int(m.group(3)))
            if message.author == ctx.guild.me:
                if not message.embeds:
                    await message.edit(embed=new_rr)       
            res = await reaction_roles.new_reaction_roles(
                self.bot, ctx.author.id, guild.id, channel.id, message.id
            )
        print(res.__dict__) # TODO work with res
        await output.ok(ctx)

    @manage_reaction_roles.command(
        name="add", 
        aliases=["a"],
        help="Adds new reaction roles to the set message. If it's this bot's message, then it will also list the emote - role pairs", 
    )
    async def add_reaction_roles(self, ctx, message_url: str):
        m = re.search(re_url_pattern, message_url)
        if m is None:
            raise ValueError("Invalid message URL")
        guild = self.bot.get_guild(int(m.group(1)))
        channel = guild.get_channel(int(m.group(2)))
        message = await channel.fetch_message(int(m.group(3)))
        await output.respond(
            ctx,
            t="Add reaction roles", 
            d="Send an emote and ping the role you want to add, like `emote @role` or `emote role_id`. Send `done` when done", 
            c=ctx.author.color
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        done = False
        while not done:
            try:
                rr_pair_message = await self.bot.wait_for(
                    "message", timeout=30.0, check=check
                )
                if rr_pair_message.content.lower() == "done":
                    break
                await add_reaction_role(
                    self.bot, ctx, rr_pair_message, message
                )
            except TimeoutError:
                done = True

        await output.done(ctx)

def setup(bot):
    bot.add_cog(ReactionRoles(bot))

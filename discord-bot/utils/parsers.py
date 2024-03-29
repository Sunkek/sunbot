import re

from emoji import UNICODE_EMOJI
from discord.ext.commands import RoleConverter, PartialEmojiConverter, \
    PartialEmojiConversionFailure, BadArgument

RE_MESSAGE_URL = r"([0-9]+)\/([0-9]+)\/([0-9]+)"
RE_EMOTE_NAME = r":([^:\s]*)(?:::[^:\s]*)*:"

def parse_switch_opt(text):
    if text is None:
        return
    elif str(text).lower() in ("true", "1", "on"):
        return True
    elif str(text).lower() in ("false", "0", "off"):
        return False
    raise ValueError("Can't parse argument. Expected None, True or False")

async def parse_message_url(text, bot):
    m = re.search(RE_MESSAGE_URL, text)
    if m is None:
        raise ValueError("Invalid message URL")
    guild = bot.get_guild(int(m.group(1)))
    channel = guild.get_channel(int(m.group(2)))
    message = await channel.fetch_message(int(m.group(3)))
    return guild, channel, message

async def parse_reaction_role_pair(text, ctx):
    try:
        emote, role = text.split()
    except ValueError:
        raise BadArgument("Must provide an emote and a role")
    try:
        emote = await PartialEmojiConverter().convert(ctx, emote)
        name = re.search(RE_EMOTE_NAME, str(emote))
        emote = re.sub(name.group(1), "_", str(emote))  # Wiping emote name to make it compact
    except PartialEmojiConversionFailure:
        emote = str(bytes(str(emote), "utf-8")[:4], "utf-8")[0]  # Stripping skintones and other modifiers
    role = await RoleConverter().convert(ctx, role)
    return emote, role

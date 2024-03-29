from typing import Union
from random import choice, seed

from discord import Embed, Color, Message
from discord.ext.commands import Context

MT = Embed.Empty
OK_TITLES = (
    "Done", "Success", "OK", "It worked", "There you go", "There, you happy?",
    "Alright", "Completed", "No errors", "Anything else?"
)
ERROR_TITLES = (
    "No", "Nope", "I don't think so", "Not gonna happen", "Nah", "Not likely", 
    "Fat chance", "Fuck you", "Good try, asshole", "No way", 
    "Did you really think I would do that?", "Do this shit yourself",
    "I am not your bitch", "You didn't ask nice enough", "Not doing that"
)  

async def respond(msg: Union[Context, Message], txt=None, t=MT, d=MT, c=None):
    """Send a response with provided text. Return the message object"""
    c = c or msg.author.color
    if t != MT or d != MT:
        e = Embed(title=t, description=d)
        if c: e.color = c
        return await msg.reply(txt, embed=e, mention_author=False)
    return await msg.reply(txt, mention_author=False)

async def done(msg: Union[Context, Message], text=None):
    seed()
    await respond(
        msg, 
        t=choice(OK_TITLES),
        d=str(text) if text else MT,
        c=Color.green(),
    )

async def not_done(msg: Union[Context, Message], error=None):
    seed()
    await respond(
        msg, 
        t=choice(ERROR_TITLES),
        d=str(error) if error else MT,
        c=Color.red(),
    )

async def ok(msg: Union[Context, Message]):
    if isinstance(msg, Context):
        msg = msg.message
    await msg.add_reaction("👌")
    
async def not_ok(msg: Union[Context, Message]):
    if isinstance(msg, Context):
        msg = msg.message
    await msg.message.add_reaction("✋")
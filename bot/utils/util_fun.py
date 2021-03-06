SPEND_CHARGE = """
UPDATE ping_roulette SET charges = charges - 1 
WHERE user_id = $1 AND guild_id = $2;
"""
FETCH_PR_PLAYERS = """
SELECT user_id FROM ping_roulette
WHERE plays = false AND guild_id = $1
"""
GIVE_CHARGE = """
UPDATE ping_roulette SET charges = charges + 1, won = won + 1
WHERE user_id = $1 AND guild_id = $2;
"""
CREATE_CHARGE = """
INSERT INTO ping_roulette 
VALUES($1, $2, 1, 1, true)
"""
FETCH_CHARGES = """
SELECT charges FROM ping_roulette
WHERE user_id = $1 AND guild_id = $2
"""
OPT_OUT = """
UPDATE ping_roulette SET plays = 'f', charges = 0
WHERE user_id = $1 AND guild_id = $2;
"""
FETCH_ACTIVE_PLAYERS = """
SELECT user_id FROM ping_roulette
WHERE charges > 0 AND plays = 't' AND guild_id = $1
"""
FETCH_BORN_TODAY = """
SELECT user_id FROM USERS WHERE
EXTRACT(DAY FROM birthday) = EXTRACT(DAY FROM NOW()) AND
EXTRACT(MONTH FROM birthday) = EXTRACT(MONTH FROM NOW())
"""

from asyncpg.exceptions import ForeignKeyViolationError

from utils import util_trackers

async def spend_pr_charge(bot, user_id, guild_id):
    """Spend user's ping roulette charge"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            res = await connection.execute(SPEND_CHARGE, user_id, guild_id)
            return not " 0" in res

async def opted_out_of_pr(bot, guild_id):
    """Fetch a list of members that don't play PR"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(FETCH_PR_PLAYERS, guild_id)
            return [i["user_id"] for i in res]

async def give_pr_charge(bot, user_id, guild_id):
    """Give a PR charge to the user"""
    try:
        async with bot.db.acquire() as connection:
            async with connection.transaction():
                res = await connection.execute(GIVE_CHARGE, user_id, guild_id)
                if " 0" in res:
                    await connection.execute(CREATE_CHARGE, user_id, guild_id)
    except ForeignKeyViolationError:
        await util_trackers.create_missing_user(bot, user_id)
        await give_pr_charge(bot, user_id, guild_id)
                    
async def fetch_charges(bot, user_id, guild_id):
    """Return the PR charges of the user in the guild"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetchval(FETCH_CHARGES, user_id, guild_id)
            return res

async def opt_out_of_pr(bot, user_id, guild_id):
    """Mark the user as unpingable"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            await connection.execute(OPT_OUT, user_id, guild_id)

async def fetch_active_members(bot, guild_id):
    """Return a list of members with active ping roulette charges."""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(FETCH_ACTIVE_PLAYERS, guild_id)
            return [i["user_id"] for i in res]
                    
async def fetch_born_today(bot):
    """Return the PR charges of the user in the guild"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(FETCH_BORN_TODAY)
            return [i["user_id"] for i in res]
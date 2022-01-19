import discord

async def create(self, user:discord.User):
    db = await self.get(user)
    if not db: 
      await self.bot.pool.execute("""
      INSERT INTO economy(user_id) VALUES ($1)
      """, user.id)

async def get(self, user:discord.User):
    return await self.bot.pool.fetchrow("""
    SELECT * FROM economy WHERE user_id = $1
    """, user.id)

async def modify(self, author: discord.User, **data) -> asyncpg.Record:
    """
    Updates/Modifies the user's economy.
    Paramaters
    ----------
    author: :class:`discord.User`
        The user to modify it's economy database.
    data:
        The data kwargs are used for having custom SET statements.
    Raises
    ------
    MissingRequiredArgument
        Did not pass in a required argument.
    KeyError
        Something went wrong in the database
    Returns
    -------
    asyncpg.Record
        The record for the updated row.
    """
    if not data:
        raise MissingRequiredArgument('**data needs to be present.')

    try:
        db = await self.bot.pool.fetchrow(f'SELECT * FROM economy WHERE user_id={author.id}')
    except Exception as exc:
        raise KeyError(exc) from exc

    if db is None:
        raise KeyError('Column user_id with %s does not exist.' % author.id)
    else:
        db = dict(db)

    db.update(data)

    try:
        db.pop('user_id')
    except KeyError:
        pass

    if not db:
        raise MissingRequiredArgument('**data needs to be present.')

    c = 2
    s = ''

    for k, v in db.items():
        s += f'{k}=${c}, '
        c += 1

    s = s[:-2]

    try:
        updated = await self.bot.pool.fetchrow(f"""
        UPDATE economy
        SET {s}
        WHERE user_id=$1
        RETURNING *
        """, author.id, *[v for k, v in db.items()])
    except Exception as exc:
        raise exc(exc) from exc
    else:
        return updated
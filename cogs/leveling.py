import math
from typing import *

import discord
from discord.ext import commands

from data import db
from files.emoji import CustomEmoji


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='레벨', aliases=['level'])
    async def level(self, ctx: commands.Context):
        user = ctx.author

        level: float = math.ceil(db.database.Player(user.id).level)
        length = len(str(level).replace('-', ''))
        if length > 32:
            length -= 1
            tox = 10 ** length
            mon = money / tox
            money = f"{mon}E{length}"
        embed = discord.Embed(
            description=f"{user.mention}님은 현재 **{level}** 레벨 입니다.",
            color=discord.Colour.blurple()
        )
        print(level)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not db.database.Player(message.author.id).verified:
            return
        if message.content.startswith("r/"):
            return
        player = db.database.Player(message.author.id)
        prev_level = player.level
        level = math.ceil(prev_level)
        new_level = player.level + 1 / (6 * math.sqrt((4 * math.floor(x))) + 1)
        if math.ceil(new_level) > math.ceil(prev_level):
            print(new_level)
            await message.add_reaction(emoji=CustomEmoji.levelup)
        player.level = new_level

def setup(bot):
    bot.add_cog(Leveling(bot))

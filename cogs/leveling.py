import math
from typing import *

import discord
from discord.ext import commands

from data import db
from files.emoji import CustomEmoji

def calc_level(level):
    return 6 * math.pow((4 * math.floor(level + 1)), 0.8) + 1

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='레벨', aliases=['level'])
    async def level(self, ctx: commands.Context):
        user = ctx.author

        lexp = db.database.Player(user.id).level
        level: float = math.floor(lexp)
        length = len(str(level).replace('-', ''))
        if length > 32:
            length -= 1
            tox = 10 ** length
            mon = level / tox
            level = f"{mon}E{length}"
        embed = discord.Embed(
            description=f"{user.mention}님은 현재 **{level}** 레벨 입니다.",
            color=discord.Colour.blurple()
        )
        totalexp = calc_level(level)
        embed.set_footer(text=f"다음 레벨 업 까지: {math.floor((lexp % 1) * totalexp)} / {math.ceil(totalexp)} 채팅")
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not db.database.Player(message.author.id).verified:
            return

        if message.content.startswith("r/"):
            return

        player = db.database.Player(message.author.id)
        prev_level = player.level
        level = math.floor(prev_level)
        new_level = player.level + 1 / calc_level(level)

        if math.floor(new_level) > math.floor(prev_level):
            await message.add_reaction(emoji=CustomEmoji.levelup)

        player.level = new_level

def setup(bot):
    bot.add_cog(Leveling(bot))

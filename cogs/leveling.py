import math
from typing import *

import discord
from discord.ext import commands

from data import db
from files.emoji import CustomEmoji


def calc_level(level):
    flr = (4 * math.floor(level + 1))
    plma = 1
    if flr < 0:
        plma = -1
    return plma * 8 * math.pow(abs(flr), 0.9) + 2


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='레벨', aliases=['level'])
    async def level(self, ctx: commands.Context):
        ...

    @level.command(name="확인", aliases=["check"])
    async def check_level(self, ctx, user: Union[discord.Member, discord.User, None] = None):
        userstr = user
        if user == None:
            user = ctx.author
        else:
            if type(user) not in [discord.User, discord.Member]:
                embed = discord.Embed(
                    description=f"🛑 **{userstr}** 유저를 찾을 수 없습니다.",
                    color=discord.Colour.red()
                )
                await ctx.send(embed=embed)
                return
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

    @level.command(name="요구수", aliases=["requires"])
    async def requires(self, ctx, level: int):
        requires = 0

        if level < 100000:
            for i in range(0, level):
                requires += calc_level(level)
        else:
            try:
                requires = math.pow(level, 1.8999) / 0.03585
            except OverflowError:
                embed = discord.Embed(
                    description=f"{level} 레벨까지 요구되는 메시지 수\n**우주가 멸망하고 다시 생겨날 만큼**",
                    color=discord.Colour.blurple()
                )
                await ctx.send(embed=embed)
                return

        embed = None

        if requires < 2 ** 64:
            embed = discord.Embed(
                description=f"{level} 레벨까지 요구되는 메시지 수\n총 **{math.floor(requires)}** 건",
                color=discord.Colour.blurple()
            )
        elif requires < 2 ** 74:
            embed = discord.Embed(
                description=f"{level} 레벨까지 요구되는 메시지 수\n**세상의 모든 별의 수보다 많이**",
                color=discord.Colour.blurple()
            )
        elif requires < 2 ** 80:
            embed = discord.Embed(
                description=f"{level} 레벨까지 요구되는 메시지 수\n**두더지 하나에 들어있는 입자의 양보다 많이**",
                color=discord.Colour.blurple()
            )
        elif requires < 2 ** 130:
            embed = discord.Embed(
                description=f"{level} 레벨까지 요구되는 메시지 수\n**영겁의 시간이 지날 만큼**",
                color=discord.Colour.blurple()
            )
        elif requires < 2 ** 335:
            embed = discord.Embed(
                description=f"{level} 레벨까지 요구되는 메시지 수\n**우주에 어떤 살아있는 것도 남아있지 않을 만큼**",
                color=discord.Colour.blurple()
            )
        elif requires < 2 ** 400:
            embed = discord.Embed(
                description=f"{level} 레벨까지 요구되는 메시지 수\n**구골보다 많이**",
                color=discord.Colour.blurple()
            )
        else:
            embed = discord.Embed(
                description=f"{level} 레벨까지 요구되는 메시지 수\n**우주가 멸망하고 다시 생겨날 만큼**",
                color=discord.Colour.blurple()
            )


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

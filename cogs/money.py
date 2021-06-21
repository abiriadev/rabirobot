from typing import Union
import discord
from discord.ext import commands

from database import db
from files import utils
from files.emoji import CustomEmoji

class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO 타입 체크 익셉션 핸들링
    @commands.command(name='돈', aliases=['money'])
    async def show_money(self, ctx: commands.Context, user: Union[discord.Member, discord.User, int, str] = None):
        if user is None:
            user = ctx.author

        money = db.players[user.id].money
        length = len(str(money))

        if length > 32:
            length -= 1
            tox = 10 ** length
            mon = money / tox
            money = f"{mon}E{length}"

        embed = discord.Embed(
            description=f"{user.mention}님의 라비머니는 현재 **{money}**{CustomEmoji.money} 입니다.",
            color=discord.Colour.blurple()
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Money(bot))

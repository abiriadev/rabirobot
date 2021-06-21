from typing import *

from database import db
from files.emoji import CustomEmoji
from files.utils import *


class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='돈', aliases=['money'])
    async def money(self, ctx: commands.Context):
        ...

    @money.command(name='보기', aliases=['show'])
    async def show_money(self, ctx: commands.Context, user: Union[discord.Member, discord.User, int, str, None] = None):
        userstr = user
        if user is None:
            user = ctx.author
        else:
            if type(user) not in [discord.User, discord.Member]:
                embed = discord.Embed(
                    description=f"🛑 **{userstr}** 유저를 찾을 수 없습니다.",
                    color=discord.Colour.red()
                )
                await ctx.send(embed=embed)
                return

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
        print(money)
        await ctx.send(embed=embed)

    @money.command(name='주기', aliases=['give'])
    async def give_money(self, ctx: commands.Context, user: Union[discord.Member, discord.User, int, str, None], amount: Optional[int]):
        userstr = user
        if amount is None:
            await send_not_enough_args(ctx, 1, "<유저>", "<수량>")
            return

        if type(user) not in [discord.User, discord.Member]:
            embed = discord.Embed(
                description=f"🛑 **{userstr}** 유저를 찾을 수 없습니다.",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return
        ...


def setup(bot):
    bot.add_cog(Money(bot))

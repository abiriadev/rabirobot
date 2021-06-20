from files import utils
import discord

from database import db
from discord.ext import commands


class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='돈', aliases=['money'])
    async def ping(self, ctx: commands.Context, user = None):
        userstr = user
        if user is None:
            user: discord.User = ctx.author
        else:
            user: discord.User   = utils.parseUser(ctx.guild, user)
            if user == None:
                embed = discord.Embed(
                    description=f"**{userstr}** 유저를 찾을 수 없습니다.",
                    color=0xF03A17
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
            description=f"{user.mention}님의 라비머니는 현재 **{money}**<:rabirocoin:855796110128185344> 입니다.",
            color=discord.Colour.blurple()
        )
        print(money)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Money(bot))

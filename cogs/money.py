from typing import *

import discord
from discord.ext import commands

from data import db
from files.emoji import CustomEmoji


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

        money = db.database.Player(user.id).money
        length = len(str(money).replace('-', ''))
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
    async def give_money(self, ctx: commands.Context, user: Union[discord.Member, discord.User, int, str, None], amount: int):
        userstr = user

        if type(user) not in [discord.User, discord.Member]:
            embed = discord.Embed(
                description=f"🛑 **{userstr}** 유저를 찾을 수 없습니다.",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        give_from = db.database.Player(ctx.author.id)
        give_to = db.database.Player(user.id)

        if give_from.money < amount:
            embed = discord.Embed(
                description=f"🛑 돈이 충분하지 않습니다!",
                color=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        if amount < 0:
            give_from.money += amount
            embed = discord.Embed(
                description=f"산신령 <- {amount * -1}{CustomEmoji.money} <- {ctx.author.mention}",
                color=discord.Colour.red()
            )
            embed.set_footer(text="산신령이 꼼수를 쓰려는 너에게서 돈을 뺏어갔습니다!")
            await ctx.send(embed=embed)
            return


        give_from.money -= amount
        give_to.money += amount

        embed = discord.Embed(
            description=f"{ctx.author.mention} -> {amount}{CustomEmoji.money} -> {user.mention}",
            color=discord.Colour.blurple()
        )
        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Money(bot))

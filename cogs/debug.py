from typing import Union
import inspect
from pprint import pformat

import discord
from discord.ext import commands

from database import db
from files import utils
import config

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 봇의 오너(관리자)인지 체크. True면 사용 가능 False면 동전의 반대
    async def cog_check(self, ctx):
        if ctx.author.id in config.bot_owner:
            return True

    @commands.group(name='디버그', aliases=['debug', 'd', '디'])
    async def debug(self, ctx):
        ...

    @debug.command(name='저장', aliases=['save'])
    async def save(self, ctx: commands.Context):
        db.players.save()
        await ctx.send("저장했음")

    # TODO 타입 체크 익셉션 핸들링
    @debug.command(name='돈주기', aliases=['돈지급', 'givemoney'])
    async def givemoney(
        self,
        ctx: commands.Context,
        money: Union[int, None] = None,
        user: Union[discord.Member, discord.User, int, str, None] = None
    ):
        if user is None:
            user = ctx.author

        if money is None:
            await ctx.send("지급할 돈을 써")

        db.players[user.id].money += money

        await ctx.send(f"**{user.name}**에게 {money}을 줌")

    @debug.command(name='돈설정', aliases=['setmoney'])
    async def setmoney(
        self,
        ctx: commands.Context,
        money: Union[int, None] = None,
        user: Union[discord.Member, discord.User, int, str, None] = None
    ):
        if user is None:
            user = ctx.author

        if money is None:
            await ctx.send("설정할 돈을 써")

        db.players[user.id].money = money

        await ctx.send(f"**{user.name}**에게 {money}만큼 돈 줌")

    @debug.command(name='eval')
    async def eval_command(self, ctx, *, args):
        res = eval(args)
        
        if inspect.isawaitable(res): 
            output = await res
        else:
            output = res

        output = pformat(output)
        await ctx.send(f'```py\n{output}\n```')

def setup(bot):
    bot.add_cog(Debug(bot))

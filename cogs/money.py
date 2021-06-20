import discord
from database import db
from discord.ext import commands


class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='돈', aliases=['money'])
    async def ping(self, ctx: commands.context):
        embed = discord.Embed(
            description=f"{ctx.author.mention}님의 라비머니는 현재 **{db.players[ctx.author.id].money}**<:rabirocoin:855796110128185344> 입니다.",
            color=0xF03A17
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Money(bot))

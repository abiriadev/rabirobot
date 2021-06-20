import discord
from discord.ext import commands
from database import db
from files import utils


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='d_저장', aliases=['d_save'])
    async def save(self, ctx: commands.Context):
        db.players.save()
        await ctx.send("저장했음")

    @commands.command(name='d_돈주기', aliases=['d_givemoney'])
    async def givemoney(self, ctx: commands.Context, *args):
        togive: discord.User
        money: int
        if len(args) == 0:
            await ctx.send("줄 돈을 써")
            return
        elif len(args) == 1:
            togive = ctx.author
            money = args[0]
        else:
            guild: discord.Guild = ctx.guild
            user = args[0]

            togive = utils.parseUser(ctx.guild, args[0])
            if togive is None:
                await ctx.send("멤버를 찾을수 없어")
                return

            money = args[1]

        try:
            money = int(money)
        except ValueError:
            await ctx.send("그거 돈 아닌데")
            return

        db.players[togive.id].money += money

        await ctx.send(f"**{togive.name}**에게 ${money}줌")

    @commands.command(name='d_돈설정', aliases=['d_setmoney'])
    async def setmoney(self, ctx: commands.Context, *args):
        togive: discord.User
        money: int
        if len(args) == 0:
            await ctx.send("설정할 돈을 써")
            return
        elif len(args) == 1:
            togive = ctx.author
            money = args[0]
        else:
            guild: discord.Guild = ctx.guild
            user = args[0]

            togive = utils.parseUser(ctx.guild, args[0])
            if togive is None:
                await ctx.send("멤버를 찾을수 없어")
                return

            money = args[1]

        try:
            money = int(money)
        except ValueError:
            await ctx.send("그거 돈 아닌데")
            return

        db.players[togive.id].money += money

        await ctx.send(f"**{togive.name}**돈 ${money}로설정함")


def setup(bot):
    bot.add_cog(Debug(bot))

from files import utils
import discord

from database import db
from discord.ext import commands


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='투표', aliases=['vote'])
    async def vote(self, ctx: commands.Context, **kwargs):



def setup(bot):
    bot.add_cog(Vote(bot))

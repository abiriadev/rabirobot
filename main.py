import discord
from discord.ext import commands

import config

from data import db


class Main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=config.bot_prefix,
            intents=discord.Intents().all(),
            help_command=None
        )

        for extension in config.extensions:
            self.load_extension(extension)


bot = Main()
@bot.check
async def need_verify(ctx: commands.Context):
    print(ctx)
    if db.database.Player(ctx.author.id).verified:
        return True

    if ctx.message.content == "r/인증":
        return False

    await ctx.send(embed=discord.Embed(title="🛑 명령어를 사용하려면 인증하세요",
                                       description="`r/인증` 명령어로 인증할 수 있습니다.", colour=discord.Colour.red()))
    return False


bot.run(config.bot_token)

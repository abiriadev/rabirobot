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
    if db.database.Player(ctx.author.id).verified:
        return True

    if ctx.message.content in ["r/인증", 'r/동의', 'r/약관동의']:
        return True

    embed = discord.Embed(
        title="🛑 명령어를 사용하려면 인증하세요",
        description="`r/인증` 명령어로 인증할 수 있습니다.",
        colour=discord.Colour.red()
    )

    await ctx.send(embed=embed)
    return False

bad = ["시발", "병신"] # 이 안에 욕설들 들어감. 나중에 많아지면 파일 분할하는게 좋을듯.
@bot.event
async def on_message(message):
    message_content = message.content 
    for i in bad: 
        if i in message_content: 
            embed = discord.Embed(
                description=f"{message.author.mention}님이 욕설을 사용했습니다!",
                color=discord.Colour.red()
            )
            embed.set_footer(text=i[0] + '*' * (len(i) - 1) + ' 욕설이 검거되었습니다!')
            await message.channel.send(embed=embed)
            await message.delete()

    await bot.process_commands(message)

bot.run(config.bot_token)

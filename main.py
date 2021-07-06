import discord
from discord.ext import commands
from datetime import datetime, tzinfo
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

    for i in ["인증", "동의", "약관동의"]:
        if ctx.message.content.startswith(f"{config.bot_prefix[0]}{i}"):
            return True

    embed = discord.Embed(
        title="🛑 명령어를 사용하려면 인증하세요",
        description=f"`{config.bot_prefix[0]}인증` 명령어로 인증할 수 있습니다.",
        colour=discord.Colour.red()
    )

    await ctx.send(embed=embed)
    return False


bad = config.curses  # 이 안에 욕설들 들어감. 나중에 많아지면 파일 분할하는게 좋을듯.


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
            await message.delete() #BUG 403 Forbidden 50001 오류 
            #한국 디스코드봇 리스트 서버 등 봇에게 권한이 없을 경우 403 오류가 남. 이곳 말고도 오류가 나는 곳은 많을것으로 추정됨. 보기 좀 그러니까 고칩시다.

    await bot.process_commands(message)

bot.run(config.bot_token)


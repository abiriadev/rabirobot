import discord
from discord.ext import commands

import config
import os

class Main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=config.bot_prefix,
            intents=discord.Intents().all(),
            help_command=None
        )

        for extension in config.extensions:
            self.load_extension(extension)

    # TODO 정식 출시 시 이 내용 수정
    async def on_ready(self):
        os.system("cls")
        print(f'이 봇이 {self.user}({self.user.id})에 연결됐어요!')

        activity = discord.Activity(name='🐛 버그 잡는 모습', type=discord.ActivityType.watching)

        await self.change_presence(
            status=discord.Status.idle,
            activity=activity
        )

bot = Main()
bot.run(config.bot_token)



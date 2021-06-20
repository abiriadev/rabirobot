import discord
from discord.ext import commands
import config
import os

class Main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=config.bot_prefix,
            intents=discord.Intents().all()
        )

        for extension in config.extensions:
            self.load_extension(extension)

    async def on_ready(self):
        
        print(f'이 봇이 {self.user}({self.user.id})에 연결됐어요!')
        print('-----')

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game('봇 테스트')
        )

os.system("cls")
bot = Main()
bot.run(config.bot_token)

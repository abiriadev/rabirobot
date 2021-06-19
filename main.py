import asyncio
import os
import discord
from discord import message
from discord.ext import commands
from discord import User
import config


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

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game('봇 테스트')
        )

bot = Main()
bot.run(config.bot_token)
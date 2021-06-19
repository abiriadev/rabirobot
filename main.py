import asyncio
import os
import discord
from discord import message
from discord.ext import commands
from discord import User
import config


bot = commands.Bot(command_prefix='r/')
os.system("cls")

@bot.event
async def on_ready():
    print(bot.user.name, '봇이 준비되었습니다!')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('봇 테스트'))
    print('[=========]')
    print('LOG / ERROR')

@bot.command()
async def ping(ctx):
    # await ctx.send(f'퐁! / 현재 핑 : {round(bot.latency * 1000)}ms')
    await ctx.send(embed=discord.Embed(
        title=" :ping_pong: pong!",
        description=f" ping : {round(bot.latency * 1000)}ms",
        color=discord.Colour.default()))

bot.run(config.bot_token)
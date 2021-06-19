import asyncio
import os
import discord
from discord import message
from discord.ext import commands
from discord import User
import config
from googletrans import Translator
translator = Translator(service_urls=['translate.google.co.kr'])

bot = commands.Bot(command_prefix='r/')
os.system("cls")

@bot.event
async def on_ready():
    print(bot.user.name, '봇이 준비되었습니다!')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity('봇 테스트중입니다.'))
    print('[=========]')
    print('LOG / ERROR')

@bot.command()
async def ping(ctx):
    # await ctx.send(f'퐁! / 현재 핑 : {round(bot.latency * 1000)}ms')
    await ctx.send(embed=discord.Embed(
        title=" :ping_pong: pong!",
        description=f" ping : {round(bot.latency * 1000)}ms",
        color=discord.Colour.default()))
@bot.command(aliases=['trans', 'koen'])
async def translate(ctx, *, text):
    #await ctx.send('현재 해당 번역 기능은 부득이하게 구버전 번역 api를 사용하고 있어 제대로 번역이 되지 않을 수도 있습니다.\n보다 정확한 번역을 바라신다면 Google 번역 페이지를 사용해주시기 바랍니다.\nCurrently, the translation function inevitably uses the old version of the translation api, so it may not be properly translated.\nIf you would like a more accurate translation, please use the Google Translate page. \n')
    await ctx.send('언어별 번역 기능은 추후 추가될 예정입니다.')
    await ctx.send(embed=discord.Embed(
        title="경고! / warning!",
        description=f"현재 해당 번역 기능은 부득이하게 구버전 번역 api를 사용하고 있어 제대로 번역이 되지 않을 수도 있습니다.\n보다 정확한 번역을 바라신다면 Google 번역 페이지를 사용해주시기 바랍니다.\n\nCurrently, the translation function inevitably uses the old version of the translation api, so it may not be properly translated.\nIf you would like a more accurate translation, please use the Google Translate page.",
        color=discord.Colour.red()))
    language = translator.detect(text).lang

    if language == 'ko' : 
        result = translator.translate(text).text
        pronunciation = translator.translate(text).pronunciation
    else:
        result = translator.translate(text, dest = 'ko').text
        pronunciation = translator.translate(text, dest = 'ko').pronunciation
    await ctx.send(embed=discord.Embed(
        title='**번역 결과 / Translation result**\n\n"'+result+'" \n',
        description=f'"{pronunciation}"\n 번역 결과는 정확하지 않을 수 있습니다. \n Translation results may not be accurate. \n https://translate.google.com/',
        color=discord.Colour.blurple()))

bot.run(config.bot_token)

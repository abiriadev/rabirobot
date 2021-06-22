import discord
import youtube_dl
from discord.ext import commands

bot = commands.Bot(command_prefix = "!")

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    if bot.voice_clients == []:
        await channel.connect()
        await ctx.send("connected to the voice channel, " + str(bot.voice_clients[0].channel))

    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = bot.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
@bot.command()
async def leave(ctx):
    await bot.voice_clients[0].disconnect()
@bot.command()
async def pause(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("already paused")

@bot.command()
async def resume(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
        await ctx.send("already playing")
        

@bot.command()
async def stop(ctx):
    if bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()
    else:
        await ctx.send("not playing")

bot.run("ODU2ODcyMDk1NTAxOTEwMDE2.YNHWUw.9ywAlf1xt3_UTHTxvY0XOPiRLyM")
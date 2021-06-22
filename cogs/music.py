import discord
from discord.ext import commands


class Music(commands.Cog):
    commands.group(name="음악", aliases=['music', 'song', '음'])
    async def music(self, ctx):
        ...
    @music.command(name="join")
    async def musicjoin(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
    
    @music.command(name="leave")
    async def leave(self, ctx):
        await music.voice_clients[0].disconnect()
    














    

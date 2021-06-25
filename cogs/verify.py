import asyncio
import datetime

import discord
from discord.ext import commands

import config
import main
from data.db import database


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.in_process = []

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.content == "r/인증":
            player = database.Player(message.author.id)
            if player.verified:
                chn: discord.TextChannel = await main.bot.fetch_channel(player.vf_message_channel)
                embed = discord.Embed(
                    title="",
                    description=f"이미 약관에 [동의](https://discord.com/channels/{chn.guild.id}/{chn.id}/{player.vf_message_id})했습니다!",
                    colour=discord.Colour.red()
                )
                await message.channel.send(embed=embed)
                return

            if message.author.id in self.in_process:
                player.vf_message_id = message.id
                player.vf_message_channel = message.channel.id
                embed = discord.Embed(
                    title="",
                    description=f"{message.author.mention}님이 약관에 동의했습니다!",
                    colour=discord.Colour.dark_teal()
                )
                embed._timestamp = datetime.datetime.utcnow()
                self.in_process.remove(message.author.id)
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Rabirobot 이용약관",
                    description="아직 아무것도 없는 것 같아 보이네요 :(\n`r/인증`을 한번 더 입력하면 약관에 동의한 것으로 간주됩니다.",
                    colour=discord.Colour.gold()
                )
                embed._timestamp = datetime.datetime.utcnow()
                await message.channel.send(embed=embed)
                self.in_process.append(message.author.id)

    @commands.command(name="인증")
    async def verify(self, ctx):
        return




def setup(bot):
    bot.add_cog(Verify(bot))

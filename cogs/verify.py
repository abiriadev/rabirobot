import asyncio
from datetime import datetime, tzinfo

import discord
from discord.ext import commands

import config
from data.db import database


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='인증', aliases=['약관동의', '동의'])
    async def verify(self, ctx):
        def check(payload):
            return str(payload.emoji) == '☑️' and ctx.author.id == payload.user_id and confirm_message.id == payload.message_id

        player = database.Player(ctx.author.id)

        if player.verified:
            channel = await self.bot.fetch_channel(player.vf_message_channel)

            embed = discord.Embed(
                description=f"이미 약관에 [동의](https://discord.com/channels/{channel.guild.id}/{channel.id}/{player.vf_message_id})했어요.",
                colour=discord.Colour.red()
            )

            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="Rabirobot 이용하기",
            description="Rabirobot을 이용하기 위해서 [서비스 이용 약관](https://www.notion.so/Rabirobot-30121c825ed34e6591698f51f6312b35)을 동의하셔야 해요.\n아래 이모지를 눌러 동의할 수 있어요.",
            colour=discord.Colour.gold()
        )
        embed._timestamp = datetime.utcnow()

        confirm_message = await ctx.send(embed=embed)
        await confirm_message.add_reaction('☑️')

        try:
            while True:
                await self.bot.wait_for('raw_reaction_add', timeout=60 * 5, check=check)

                player.vf_message_id = confirm_message.id
                player.vf_message_channel = ctx.channel.id

                kstnow = datetime.now()
                now = datetime.utcnow()
                when_verfy = kstnow.strftime('%H시 %M분 %S초 경 (UTC+9)')

                embed = discord.Embed(
                    description=f'{when_verfy} {ctx.author.mention}님이 약관에 동의하셨어요.',
                    colour=discord.Colour.dark_teal()
                )
                embed._timestamp = now
                await confirm_message.edit(embed=embed)
                break

        except asyncio.TimeoutError:
            embed = discord.Embed(
                description=f'너무 오랜 시간이 지났습니다.',
                colour=discord.Colour.dark_teal()
            )

            await confirm_message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Verify(bot))

import asyncio
from datetime import datetime
from typing import Optional

import discord
from discord.ext import commands

import config
from files.emoji import CustomEmoji
from data.db import database


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='약관', aliases=['이용약관'])
    async def tos(self, ctx):
        link = discord.ui.Button(url="https://www.notion.so/Rabirobot-30121c825ed34e6591698f51f6312b35",
                                 label="Rabirobot 이용약관",
                                 style=discord.ButtonStyle.blurple)
        view = discord.ui.View()
        view.add_item(link)
        await ctx.send(embed=discord.Embed(description="**약관 확인하기**", colour=discord.Colour.blurple()), view=view)

    @commands.command(name='인증', aliases=['약관동의', '동의'])
    async def verify(self, ctx, cancel: Optional[str] = None):
        player = database.Player(ctx.author.id)
        embed = None
        if cancel in ["취소", "철회"]:
            if player.verified:
                channel = await self.bot.fetch_channel(player.vf_message_channel)
                player.vf_message_id = None
                player.vf_message_channel = None
                embed = discord.Embed(
                    description=f"약관 [동의](https://discord.com/channels/{channel.guild.id}/{channel.id}/{player.vf_message_id})를 철회했어요.",
                    colour=discord.Colour.blurple()
                )

            else:
                embed = discord.Embed(
                    title="",
                    description=f"아직 인증되지 않은 유저에요.\n`{config.bot_prefix[0]}인증` 명령어로 인증할 수 있습니다.",
                    colour=discord.Colour.red()
                )
            await ctx.send(embed=embed)
            return
        try:
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
                description="""Rabirobot을 이용하기 위해서 [서비스 이용 약관](https://www.notion.so/Rabirobot-30121c825ed34e6591698f51f6312b35)을 동의하셔야 해요.
                아래에서 동의할 수 있어요.""",
                colour=discord.Colour.gold()
            )
            confirm_message: discord.Message = await ctx.send(embed=embed)
            embed._timestamp = datetime.utcnow()
            accept_view = discord.ui.View()
            button = discord.ui.Button(custom_id=f"confirm_{confirm_message.id}", emoji=CustomEmoji.unchecked,
                                       style=discord.ButtonStyle.gray, label="약관에 동의합니다.")
            responded = False

            async def confirm(interaction: discord.Interaction):
                if interaction.user.id != ctx.author.id:
                    await asyncio.sleep(3)
                    return
                button.style = discord.ButtonStyle.blurple
                button.emoji = CustomEmoji.checked
                button.label = "인증되었습니다."
                button.disabled = True
                responded = True
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
                await confirm_message.edit(embed=embed, view=accept_view)

            button.callback = confirm
            accept_view.add_item(button)
            await confirm_message.edit(view=accept_view)

            await asyncio.sleep(180)
            if responded:
                return
            button.style = discord.ButtonStyle.gray
            button.emoji = CustomEmoji.timeout
            button.label = "만료되었습니다."
            button.disabled = True

        except Exception as E:
            print(E.with_traceback(None))


def setup(bot):
    bot.add_cog(Verify(bot))

import datetime
import os
import random
from typing import Union

import discord
from discord.ext import commands

import config
import coroutines
from data import db
from data.vote import VoteData


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        os.system("cls")
        print(f'이 봇이 {self.bot.user}({self.bot.user.id})에 연결됐어요!')
        print("ERROR / OUTPUT")
        print("--------------")

        build_channel: discord.TextChannel = await self.bot.fetch_channel(config.build_channel)
        last_build = await build_channel.history(limit=1, oldest_first=False).flatten()
        last_build: discord.Message = last_build[0]
        if len(last_build.embeds) == 0:
            config.build = 1
        else:
            embed = last_build.embeds[0]
            try:
                config.build = int(embed.title.split('.')[-1]) + 1
            except:
                try:
                    config.build = int(embed.title.split(' ')[-1]) + 1
                except:
                    config.build = 1
            print("BUILD      |", config.identifier, config.build)
            print("VERSION    |", config.version)
            print("DEBUG MODE |", config.debug)
            print()
        config.build_string = f"{config.identifier.title()} Build {config.build}" if config.debug else f"{config.version}-{config.identifier}.{config.build}"

        build_embed = discord.Embed(title=config.build_string, color=discord.Color.random())
        build_embed._timestamp = datetime.datetime.utcnow()

        await build_channel.send(embed=build_embed)

        await coroutines.refresh_verification(self.bot)

        # TODO 정식 출시 시 이 내용 수정
        activity = discord.Activity(name='🐛 버그 잡는 모습', type=discord.ActivityType.watching)

        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=activity
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if ctx.message.content == "r/인증" or not db.database.Player(ctx.author.id).verified:
            return

        # IGNORE EXCEPTIONS
        if isinstance(error, (commands.CommandNotFound)):
            print(error)
            return
            
        # User Input Error
        elif isinstance(error, commands.MissingRequiredArgument):
            error_desctiption = '명령어를 구성하는 필수 인자가 누락되었어요. 명령어를 제대로 사용했는지 확인해 주세요.'

        elif isinstance(error, commands.BadArgument):
            error_desctiption = '입력된 인자에 문제가 생겼거나 인식할 수 없어요.'

        elif isinstance(error, commands.UserInputError):
            error_desctiption = '명령어를 잘못 사용했어요.'

        # Check Failure / Forbidden
        elif isinstance(error, commands.PrivateMessageOnly):
            error_desctiption = '이 명령어는 다이렉트 메시지에서만 사용할 수 있어요.'

        elif isinstance(error, commands.NoPrivateMessage):
            error_desctiption = '이 명령어는 다이렉트 메시지에서는 사용할 수 없어요.'

        elif isinstance(error, commands.MissingPermissions):
            error_desctiption = f'당신에게 {", ".join(error.missing_perms)} 권한이 없어요.'

        elif isinstance(error, commands.CheckFailure):
            error_desctiption = '당신은 이 명령어를 실행할 수 있는 권한이 없어요.'

        elif isinstance(error.original, discord.Forbidden):
            error_desctiption = '봇에게 명령어 실행에 필요한 권한이 없어요. 해당 명령어를 제대로 사용하기 위한 권한이 봇에게 부여되어 있는지 확인해 주세요.'

        # else - bot
        elif isinstance(error, commands.DisabledCommand):
            error_desctiption = '해당 명령어가 알 수 없는 이유로 비활성화 돼 있어요.'

        elif isinstance(error, commands.CommandOnCooldown):
            error_desctiption = f'아직 그 명령어는 쿨타임 중에 있어요. {int(error.retry_after)}초 후에 다시 시도해주세요.'

        elif isinstance(error, commands.ExtensionError):
            error_desctiption = '봇의 Extension과 관련한 오류가 발생했어요. 봇 개발자에게 문의해 주세요.'

        # code, system
        elif isinstance(error.original, (
        IndexError, KeyError, NameError, OSError, SyntaxError, TabError, SystemError, TypeError, UnicodeError,
        ValueError, AttributeError)):
            error_desctiption = '문법적인 오류가 발생했어요.'

        else:
            error_desctiption = '예기치 못한 오류가 발생했어요.'

        embed = discord.Embed(
            title=f'🛑 {error_desctiption}',
            color=0xF03A17
        )
        await ctx.send(embed=embed)

        if config.debug:
            raise error

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        reaction: discord.RawReactionActionEvent = payload
        user: Union[discord.Member, discord.User] = await self.bot.fetch_user(payload.user_id)
        if user == self.bot.user:
            return

        no_two_react = []
        for vote in db.database.votes.keys():
            vote: VoteData = db.database.Vote(vote)
            no_two_react.append(vote.messageId)

        if reaction.message_id in no_two_react:
            chn: discord.TextChannel = await self.bot.fetch_channel(reaction.channel_id)
            msg: discord.Message = await chn.fetch_message(reaction.message_id)
            for r in msg.reactions:
                if r.emoji == payload.emoji:
                    continue
                if user in await r.users().flatten():
                    await msg.remove_reaction(r.emoji, user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        reaction: discord.RawReactionActionEvent = payload
        user: Union[discord.Member, discord.User] = await self.bot.fetch_user(payload.user_id)

        player = db.database.Player(user.id)

        if str(reaction.emoji) == '☑️' and player.vf_message_id == payload.message_id:
            print("asdf")
            chn: discord.TextChannel = await self.bot.fetch_channel(reaction.channel_id)
            msg: discord.Message = await chn.fetch_message(reaction.message_id)

            kstnow = datetime.datetime.now()
            now = datetime.datetime.utcnow()
            when_verfy = kstnow.strftime('%H시 %M분 %S초 경 (UTC+9)')

            embed = msg.embeds[0]
            embed.description += f'\n\n{when_verfy} 약관 동의를 취소하셨어요.'
            embed.color = discord.Colour.red()
            embed._timestamp = now
            player.vf_message_id = None
            player.vf_message_channel = None

            await msg.edit(embed=embed)
            await msg.clear_reaction('☑️')



def setup(bot):
    bot.add_cog(EventHandler(bot))

import os

import discord
from discord.ext import commands


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        os.system("cls")
        print(f'이 봇이 {self.bot.user}({self.bot.user.id})에 연결됐어요!')

        # TODO 정식 출시 시 이 내용 수정
        activity = discord.Activity(name='🐛 버그 잡는 모습', type=discord.ActivityType.watching)

        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=activity
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, (commands.CommandNotFound)):
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
            error_desctiption = '봇에게 명령어 실행에 필요한 권한이 없없어요.'

        # else - bot
        elif isinstance(error, commands.DisabledCommand):
            error_desctiption = '해당 명령어가 알 수 없는 이유로 비활성화 돼 있어요.'
            
        elif isinstance(error, commands.CommandOnCooldown):
            error_desctiption = f'아직 그 명령어는 쿨타임 중에 있어요. {int(error.retry_after)}초 후에 다시 시도해주세요.'
        
        elif isinstance(error, commands.ExtensionError):
            error_desctiption = '봇의 Extension과 관련한 오류가 발생했어요. 봇 개발자에게 문의해 주세요.'
            
        # code, system
        elif isinstance(error.original, (IndexError, KeyError, NameError, OSError, SyntaxError, TabError, SystemError, TypeError, UnicodeError, ValueError, AttributeError)):
            error_desctiption = '문법적인 오류가 발생했어요.'
            
        else:
            error_desctiption = '예기치 못한 오류가 발생했어요.'
            
        embed = discord.Embed(
            title=f'🛑 {error_desctiption}',
            color=0xF03A17
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(EventHandler(bot))
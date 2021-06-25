from typing import Union
import inspect
from pprint import pformat

import discord
from discord.ext import commands

from database import db
from files import utils
import config


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 봇의 오너(관리자)인지 체크. True면 사용 가능 False면 동전의 반대
    async def cog_check(self, ctx):
        if ctx.author.id in config.bot_owner:
            return True

    @commands.group(name='디버그', aliases=['debug', 'd', '디'])
    async def debug(self, ctx):
        ...

    @debug.command(name='help', aliases=['도움말', '도움', '도', 'ㄷ', '명령어', '커맨드', 'commands', 'command', 'h'])
    async def db_help(self, ctx):
        embed = discord.Embed(
            title="🛠 도움말",
            description=f"""[디버그 : 명령어 모음]
            저장   : 변경된 정보를 저장함.
            돈주기 : 입력한 수만큼 선택 유저에게 돈을 지급(-도 가능.)
            도움말 : 이 도움말 메세지를 표시함.
            돈설정 : 선택한 유저의 돈의 데이터를 덮어씌움.
            eval  : 파이썬의 eval 함수를 실행시킴.
            info  : 봇 정보를 출력함
            """,
            color=discord.Colour.red()
        )

        await ctx.send("디버그 도움말을 DM으로 보냈어요. 전송되지 않았을 경우, 다이렉트 메시지를 막아 두었는지 확인해 주세요.")
        await ctx.author.send(embed=embed)

    @debug.command(name='저장', aliases=['save'])
    async def save(self, ctx: commands.Context):
        db.database.save()
        await ctx.send("저장했음")

    # TODO 타입 체크 익셉션 핸들링
    @debug.command(name='돈주기', aliases=['돈지급', 'givemoney'])
    async def givemoney(
            self,
            ctx: commands.Context,
            money: Union[int, None] = None,
            user: Union[discord.Member, discord.User, int, str, None] = None
    ):
        if user is None:
            user = ctx.author

        if money is None:
            await ctx.send("지급할 돈을 써")

        db.database.Player(user.id).money += money

        await ctx.send(f"**{user.name}**에게 {money}을 줌")

    @debug.command(name='돈설정', aliases=['setmoney'])
    async def setmoney(
            self,
            ctx: commands.Context,
            money: Union[int, None] = None,
            user: Union[discord.Member, discord.User, int, str, None] = None
    ):
        if user is None:
            user = ctx.author

        if money is None:
            if user is None:
                await ctx.send("설정할 돈을 써")
        db.database.Player(user.id).money = money

        await ctx.send(f"**{user.name}**에게 {money}로 돈 설정함")


    @debug.command(name='돈초기화', aliases=['resetmoney'])
    async def resetmoney(self, ctx: commands.Context):
        for i in db.database.players.keys():
            db.database.Player(i).money = 0
        await ctx.send(f"다 돈 0댐 ㅅㄱ")


    @debug.command(name='eval')
    async def eval_command(self, ctx, *, args: str):
        res = eval(args)

        if inspect.isawaitable(res):
            output = await res
        else:
            output = res

        if not (
                'token' in args.lower() or
                'secret' in args.lower() or
                'config' in args.lower() or
                config.bot_token in str(output)
        ):
            embed = discord.Embed(
                title='📝 Eval',
                color=0xFDCE4C
            )

            embed.add_field(name='📥 인풋', value=f'```py\n{args}```', inline=False)
            embed.add_field(name='📤 아웃풋', value=f'```py\n{pformat(output)}```')
            embed.add_field(name='🔍 타입', value=f'```py\n{type(output)}```')

        elif (
                'eval' in args.lower() or
                'exec' in args.lower()
        ):
            embed = discord.Embed(
                title='🛑 제한됨',
                description='eval이나 exec 등은 사용할 수 없습니다.',
                color=discord.Colour.red()
            )

        else:
            embed = discord.Embed(
                title='🛑 제한됨',
                description='민감한 정보는 전송할 수 없습니다.',
                color=discord.Colour.red()
            )

        await ctx.send(embed=embed)

    @debug.command(name="version", aliases=['ver', 'info', '버전', '정보'])
    async def botversion(self, ctx):
        info = discord.Embed(
                title='Bot info',
                description="",
                color=discord.Colour.red()
            )

        info.add_field(name="Version", value=config.build_string, inline=False)
        info.add_field(
                        name="Developers",
                        value=
                        '''kainaght
                            papertoy1127
                            ppapman1
                            321PLEK
                            Abiria''',
                        inline=False
                        )

        info.set_thumbnail(url="https://cdn.discordapp.com/avatars/855652837236670464/334c3952a503bc101b8ced247a335c05.webp?size=256")

        await ctx.send(
            embed=info
        )


def setup(bot):
    bot.add_cog(Debug(bot))

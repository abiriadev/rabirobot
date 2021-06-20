import discord
from discord.ext import commands
from googletrans import Translator


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator(service_urls=['translate.google.co.kr'])

    @commands.command(name='핑', aliases=['ping'])
    async def ping(self, ctx):
        embed = discord.Embed(
            title="🏓 퐁!",
            description=f"봇의 레이턴시 : {round(self.bot.latency * 1000)}ms",
            color=0xF03A17
        )

        await ctx.send(embed=embed)

    # BUG self.translator.detect(text)에 AttributeError: 'NoneType' object has no attribute 'group' 오류
    #  googleTrans 모듈의 버전 문제, 구버전으로 설치 후 문제 없음 확인
    @commands.command(name='번역', aliases=['trans', 'translate'])
    async def translate_command(self, ctx, *, text):
        await ctx.trigger_typing()

        language = self.translator.detect(text).lang
        translate = self.translator.translate

        if language == 'ko':
            translate_result = translate(text)

            result_text = translate_result.text
            result_pronunciation = translate_result.pronunciation

        else:
            translate_result = translate(text, dest='ko')

            result_text = translate_result.text
            result_pronunciation = translate_result.pronunciation

        embed = discord.Embed(
            title='번역 결과',
            description=f'''번역 결과는 정확하지 않을 수 있습니다.

            [구글 번역기](https://translate.google.com/)''',
            color=discord.Colour.blurple()
        )

        embed.add_field(name=result_text, value=f'"{result_pronunciation}"')

        await ctx.send(embed=embed)

    @commands.command(name='bothelp', aliases=['도움말', 'h', 'b_help'])
    async def bothelp(self, ctx):
        embed = discord.Embed(
        title="🛠 도움말",
        description=f"[명령어 모음] \n ※ 접두사는 r/입니다. ※ \n 핑 : 봇의 레이턴시를 출력합니다. \n 번역 : googletrans를 이용해 외국어를 한국어로 번역합니다. \n 도움말 : 이 도움말 메세지를 표시합니다. \n 돈 : 보유 중인 라비머니를 표시합니다. \n",
        color=0xF03A17
        
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Chat(bot))

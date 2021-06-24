import random
from typing import Union, Optional

from files import utils
import discord

from database import db
from discord.ext import commands

from files.emoji import numbers


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='투표', aliases=['vote'])
    async def vote(self, ctx):
        ...


    @vote.command(name='만들기', aliases=['create', 'new', '제작'])
    async def create_vote(self, ctx: commands.Context, channel: Union[discord.TextChannel, None], title='제목 없는 투표', desc=''):
        if channel is None:
            channel = ctx.channel
        if title is None:
            title="제목 없는 투표"
        if desc is None:
            desc=""
        if channel.id in db.database.votes.keys():
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 이미 진행 중인 투표가 있습니다!", color=discord.Colour.red()))
            return
        vote = db.database.Vote(channel.id)
        vote.title = title
        vote.description = desc

        await ctx.send(embed=vote.preview)

    @vote.command(name='프리뷰', aliases=['preview'])
    async def preview(self, ctx: commands.Context, channel: Union[discord.TextChannel, None]):
        if channel is None:
            channel = ctx.channel

        if channel.id not in db.database.votes.keys():
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 채널에 진행 중인 투표가 없습니다!", color=discord.Colour.red()))
            return
        vote = db.database.Vote(channel.id)
        await ctx.send(embed=vote.preview)

    @vote.group(name='항목', aliases=['item'])
    async def item(self, ctx: commands.Context):
        ...

    @item.command(name='추가', aliases=['add'])
    async def add(self, ctx, channel: Union[discord.TextChannel, None], value: str):
        if channel is None:
            channel = ctx.channel

        if channel.id not in db.database.votes.keys():
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 채널에 제작 중인 투표가 없습니다!", color=discord.Colour.red()))
            return
        vote = db.database.Vote(channel.id)

        if vote.published:
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 이미 시작된 투표에 항목을 추가할 수 없습니다!", color=discord.Colour.red()))
            return

        vote.fields.append(value)

    @item.command(name='삭제', aliases=['remove', 'delete', '제거'])
    async def remove(self, ctx: commands.Context, channel: Union[discord.TextChannel, None], value: Optional[str]):
        if channel is None:
            channel = ctx.channel

        if channel.id not in db.database.votes.keys():
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 채널에 제작 중인 투표가 없습니다!", color=discord.Colour.red()))
            return
        vote = db.database.Vote(channel.id)

        if vote.published:
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 이미 시작된 투표에서 항목을 삭제할 수 없습니다!", color=discord.Colour.red()))
            return

        if value is None:
            vote.fields.pop()
            return
        try:
            value = int(value)
            del vote.fields[value - 1]
        except:
            vote.fields.remove(value)

    @vote.command(name="발행", aliases=['publish', 'start', '시작'])
    async def publish(self, ctx, channel: Union[discord.TextChannel, None]):
        if channel is None:
            channel = ctx.channel

        if channel.id not in db.database.votes.keys():
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 채널에 제작 중인 투표가 없습니다!", color=discord.Colour.red()))
            return
        vote = db.database.Vote(channel.id)

        if vote.published:
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 투표가 이미 시작되었습니다!", color=discord.Colour.red()))
            return

        msg: discord.Message = await ctx.send(embed=vote.embed)
        vote.messageId = msg.id
        lfields = len(vote.fields) - 1
        for i in range(abs(lfields) // 20):
            tmp = await ctx.send('⠀')
            vote.additionalMessages.append(tmp.id)

        n = 1
        for i in vote.fields:
            if n <= 20:
                await msg.add_reaction(numbers[n])
            else:
                msg = await channel.fetch_message(vote.additionalMessages[((n-1) // 20) - 1])
                bot: commands.Bot = self.bot
                emoj = random.choice(bot.emojis)
                print(emoj)
                while emoj in numbers:
                    emoj = random.choice(bot.emojis)
                await msg.add_reaction(emoj)
            n += 1
        vote.published = True

    @vote.command(name="종료", aliases=['finish', 'stop', '끝'])
    async def finish(self, ctx, channel: Union[discord.TextChannel, None]):
        if channel is None:
            channel = ctx.channel

        if channel.id not in db.database.votes.keys():
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 채널에 진행 중인 투표가 없습니다!", color=discord.Colour.red()))
            return
        vote = db.database.Vote(channel.id)

        if not vote.published:
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 투표가 시작되지 않았습니다!", color=discord.Colour.red()))
            return

        msg: discord.Message = await channel.fetch_message(vote.messageId)

        result = discord.Embed(title=f"투표 결과", description="", colour=discord.Colour.blurple())
        n = 1
        result.description += "\n"
        for r in msg.reactions:
            r: discord.Reaction = r
            result.description += f"\n**[{n}]** {vote.fields[n - 1]} => {r.count - 1}명"
            n += 1
            await msg.clear_reaction(r)
        for m in vote.additionalMessages:
            m = await channel.fetch_message(m)
            for r in m.reactions:
                r: discord.Reaction = r
                result.description += f"\n**[{n}]** {vote.fields[n - 1]} => {r.count - 1}명"
                n += 1
                await m.clear_reaction(r)
        msg.embeds[0].description = vote.description + result.description
        msg.embeds[0].title += " (종료됨)"
        result.description = f"[투표 보기](https://discord.com/channels/{channel.guild.id}/{channel.id}/{vote.messageId})" + result.description

        await msg.edit(embed=msg.embeds[0])
        db.database.votes.pop(channel.id)
        await ctx.send(embed=result)
    @vote.command(name='help', aliases=['도움말', '도움', '도', 'ㄷ', '명령어', '커맨드', 'commands', 'command', 'h'])
    async def help(self, ctx):
        embed = discord.Embed(
            title="📋 투표 도움말",
            description=f"""**투표 명령어 모음**
            투표 만들기 : 새로운 투표를 생성합니다.
            투표 프리뷰 : 투표 발행 전 프리뷰를 표시합니다.
            도움말 : 이 도움말 메세지를 표시합니다.
            투표 항목 추가 : 투표의 항목을 추가합니다.
            투표 항목 삭제 : 투표의 항목을 제거합니다.
            투표 발행 : 투표를 발행합니다.
            투표 종료 : 진행중인 투표를 종료합니다.
            자세한 도움말은 [__Rabirobot 위키__](https://github.com/KaiNiGHt/rabirobotdocs/wiki)를 확인해주세요.
            """,
            color=discord.Colour.red()
        )
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Vote(bot))

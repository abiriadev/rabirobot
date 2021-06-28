import random
from typing import Union, Optional

import discord

from data import db
from discord.ext import commands

from files.emoji import CustomEmoji


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(name='투표', aliases=['vote'])
    async def vote(self, ctx):
        ...

    @vote.command(name='만들기', aliases=['create', 'new', '제작'])
    async def create_vote(self, ctx: commands.Context, channel: Union[discord.TextChannel, None], title='제목 없는 투표',
                          desc=''):
        if channel is None:
            channel = ctx.channel
        if title is None:
            title = "제목 없는 투표"
        if desc is None:
            desc = ""
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

        if len(vote.fields) >= 20:
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 투표의 항목은 최대 20개까지 가능합니다!", color=discord.Colour.red()))
            return

        vote.fields.append(value)
        await ctx.send(
            embed=discord.Embed(title="", description=f"투표에 {value} 항목을 추가하였습니다.", color=discord.Colour.blurple()))
        return

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
            if len(vote.fields) == 0:
                await ctx.send(
                    embed=discord.Embed(title="", description="🛑 투표에 항목이 없습니다!", color=discord.Colour.red()))
            else:
                await ctx.send(
                    embed=discord.Embed(title="", description="투표에서 마지막 항목을 제거하였습니다.", color=discord.Colour.blurple()))
                vote.fields.pop()
            return
        try:
            value = int(value)
        except:
            if value in vote.fields:
                vote.fields.remove(value)
                await ctx.send(
                    embed=discord.Embed(title="", description=f"투표에서 {value} 항목을 제거하였습니다.", color=discord.Colour.blurple()))
            else:
                await ctx.send(
                    embed=discord.Embed(title="", description=f"투표에 {value} 항목이 없습니다.",
                                        color=discord.Colour.blurple()))
            return
        try:
            del vote.fields[value - 1]
            await ctx.send(
                embed=discord.Embed(title="", description=f"투표에서 {value}번째 항목을 제거했습니다.",
                                    color=discord.Colour.blurple()))
        except:
            await ctx.send(
                embed=discord.Embed(title="", description=f"투표에 {value}번째 항목이 없습니다.",
                                    color=discord.Colour.blurple()))

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

        n = 1
        for i in vote.fields:
            await msg.add_reaction(CustomEmoji.numbers[n])
            n += 1

        vote.published = True

    @vote.command(name="종료", aliases=['finish', 'end', '끝'])
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
        msg.embeds[0].description = vote.description + result.description
        msg.embeds[0].title += " (종료됨)"
        result.description = f"[투표 보기](https://discord.com/channels/{channel.guild.id}/{channel.id}/{vote.messageId})" + result.description

        await msg.edit(embed=msg.embeds[0])
        db.database.votes.pop(channel.id)
        await ctx.send(embed=result)

    @vote.command(name="취소", aliases=['cancel', '안해'])
    async def cancel(self, ctx, channel: Union[discord.TextChannel, None]):
        if channel is None:
            channel = ctx.channel

        if channel.id not in db.database.votes.keys():
            await ctx.send(
                embed=discord.Embed(title="", description="🛑 채널에 진행 중인 투표가 없습니다!", color=discord.Colour.red()))
            return
        vote = db.database.Vote(channel.id)

        if vote.published:
            msg: discord.Message = await channel.fetch_message(vote.messageId)
            msg.embeds[0].title += " (취소됨)"
            await msg.clear_reactions()
            await msg.edit(embed=msg.embeds[0])
        db.database.votes.pop(channel.id)
        await ctx.send(embed=discord.Embed(description="투표가 취소되었습니다.", title="", colour=discord.Colour.magenta()))

    @vote.command(name='help', aliases=['도움말', '도움', '도', 'ㄷ', '명령어', '커맨드', 'commands', 'command', 'h'])
    async def help(self, ctx):
        embed = discord.Embed(
            title="📋 투표 도움말",
            description=f"""**투표 명령어 모음**
            투표 만들기: 새로운 투표를 생성합니다.
            투표 프리뷰: 투표 발행 전 프리뷰를 표시합니다.
            도움말: 이 도움말 메세지를 표시합니다.
            투표 항목 추가: 투표의 항목을 추가합니다.
            투표 항목 삭제: 투표의 항목을 제거합니다.
            투표 발행: 투표를 발행합니다.
            투표 종료: 발행된 투표를 종료합니다.
            투표 종료: 진행중인 투표를 취소합니다.
            자세한 도움말은 [__Rabirobot 위키__](https://github.com/KaiNiGHt/rabirobotdocs/wiki)를 확인해주세요.
            """,
            color=discord.Colour.red()
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Vote(bot))

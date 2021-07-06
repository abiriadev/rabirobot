import asyncio
import time
from typing import *

import discord
from discord.ext import commands

import data.db
import main
from files.emoji import CustomEmoji

unset = -1
red = 0
blue = 1


class DwiJipGyi(discord.ui.View):
    def __init__(self, red_team, blue_team, width=4, height=4, timelast=30, money: int = 0, message: Optional[discord.Message] = None):
        super().__init__(timeout=None)
        print(timelast)
        self.time = timelast
        self.message = message
        self.width = width
        self.height = height
        self.cards = []
        self.timeleft = timelast
        self.red_team = red_team
        self.blue_team = blue_team
        self.red_team_ids = []
        self.blue_team_ids = []
        self.money = money
        msg_red = "🟥:"
        for i in red_team:
            msg_red += f" {i.mention}"
            self.red_team_ids.append(i.id)
        msg_blue = "🟦:"
        for i in blue_team:
            msg_blue += f" {i.mention}"
            self.blue_team_ids.append(i.id)

        self.default_message = msg_red + '\n' + msg_blue + '\n' + f'판돈: {money}{CustomEmoji.money}' + '\n'
        self.embed = discord.Embed(title="", description=self.default_message)

    async def init(self):
        for x in range(self.width):
            self.cards.append([])
            for y in range(self.height):
                self.cards[x].append(None)
        for x in range(self.width):
            for y in range(self.height):
                style = discord.ButtonStyle.gray

                btn = discord.ui.Button(label=f"", style=style, custom_id=f"djg:{x}_{y}_{self.message.id}", row=x)
                btn.team = unset
                btn.emoji = CustomEmoji.empty
                btn.disabled = True
                self.add_item(btn)
                self.cards[x][y] = btn
                btn.callback = self.dwijip(x, y)
                btn.style = discord.ButtonStyle.gray
        await self.message.edit(view=self, embed=self.embed)

        for i in range(5):
            await self.message.edit(content=f"`{5 - i}`초 후 시작합니다...")
            await asyncio.sleep(1 - main.bot.latency * 2)
        for i in self.cards:
            for c in i:
                c.disabled = False

        time_started = time.time()
        await self.message.edit(view=self)
        while self.timeleft >= 1:
            await self.message.edit(content=f"`{int(self.timeleft)}`초 남았습니다!")
            await asyncio.sleep(1 - main.bot.latency * 2)
            self.timeleft = round(self.time + time_started - time.time())
        count_red = 0
        count_blue = 0
        for i in self.cards:
            for c in i:
                if c.team == red:
                    count_red += 1
                elif c.team == blue:
                    count_blue += 1
                card: discord.ui.Button = c
                card.disabled = True
        win = "🟥 승리!" if count_red > count_blue else "🟦 승리!" if count_red < count_blue else "🟥 무승부! 🟦"
        await self.message.edit(view=self, content=f"🟥 {count_red} vs {count_blue} 🟦\n{win}")

        if win == "🟥 승리!":
            for b in self.blue_team:
                data.db.database.Player(b.id).money -= self.money
            for r in self.red_team:
                data.db.database.Player(r.id).money += self.money
        elif win == "🟦 승리!":
            for b in self.blue_team:
                data.db.database.Player(b.id).money += self.money
            for r in self.red_team:
                data.db.database.Player(r.id).money -= self.money

    def dwijip(self, x, y):
        async def result(inte: discord.Interaction):
            if (inte.user.id in self.red_team_ids) or (inte.user.id in self.blue_team_ids):
                card: discord.ui.Button = self.cards[x][y]
                '''
                color = (card.team + 1) % 2
                card.team = color
                style = discord.ButtonStyle.red
                if color == 1:
                    style = discord.ButtonStyle.blurple
                card.style = style'''

                if inte.user.id in self.red_team_ids:
                    card.team = red
                    card.style = discord.ButtonStyle.red
                else:
                    card.team = blue
                    card.style = discord.ButtonStyle.blurple

                await self.message.edit(view=self)
            else:
                await inte.response.send_message(ephemeral=True, content='🛑 게임에 참여중이 아닙니다!')

        return result

class Teselect(discord.ui.View):
    def __init__(self, message: Optional[discord.Message] = None):
        super().__init__(timeout=None)
        self.message = message

    @discord.ui.select(placeholder="sans", custom_id="teselect:asdf",
                       options=[discord.SelectOption(label="wa", value="와"),
                                discord.SelectOption(label="sans", value="샌즈"),
                                discord.SelectOption(label="asineunguna", value="아시는구나")])
    async def wasans(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.name}님이 {interaction.data['values'][0]} 선택함")


def sendInteraction(content):
    async def result(interaction: discord.Interaction):
        await interaction.response.send_message(content, ephemeral=True)

    return result

class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='실험', aliases=['testing', 'experiment', 'expm'])
    async def testing(self, ctx: commands.Context):
        ...

    @testing.command(name='아무기능', aliases=['random'])
    async def random(self, ctx: commands.Context):
        await ctx.send()

    @testing.command(name='뒤집기', aliases=['flip'])
    async def button(self, ctx: commands.Context, x: int, y: int, timelast, money: int, *players: discord.Member):
        if len(players) % 2 == 1:
            await ctx.send(embed=discord.Embed(title=f'🛑 플레이어 수가 홀수일 수 없습니다!', color=discord.Color.red()))
            return
        mid = len(players) // 2
        red_team = players[0:mid]
        blue_team = players[mid:]

        if timelast is None:
            timelast = 30
        else:
            try:
                timelast = float(timelast)
            except:
                if timelast.endswith('초') or timelast.endswith('s'):
                    try:
                        timelast = float(timelast[:-1])
                    except:
                        raise commands.BadArgument()
                elif timelast.endswith('분') or timelast.endswith('m') or timelast.endswith('min'):
                    try:
                        timelast = float(timelast[:-1]) * 60
                    except:
                        raise commands.BadArgument()
                elif timelast.endswith('시간'):
                    try:
                        timelast = float(timelast[:-2]) * 60 * 60
                    except:
                        raise commands.BadArgument()
                elif timelast.endswith('h') or timelast.endswith('시'):
                    try:
                        timelast = float(timelast[:-2]) * 60 * 60
                    except:
                        raise commands.BadArgument()
        print(timelast)
        if timelast < 1:
            await ctx.send(embed=discord.Embed(title=f'🛑 너무 짧은 시간을 설정했습니다!', color=discord.Color.red()))
            return
        if timelast > 360:
            await ctx.send(embed=discord.Embed(title=f'🛑 너무 긴 시간을 설정했습니다!', color=discord.Color.red()))
            return

        nem = ""
        for i in players:
            if data.db.database.Player(i.id).money < money:
                nem += i.mention + ", "
        if len(nem) > 0:
            nem = nem[:-2]
            await ctx.send(embed=discord.Embed(title=f'''🛑 {nem}님의 라비머니가 {money}{CustomEmoji.money}보다 적습니다.
게임에서 패배하면 빚을 지게 됩니다.''', color=discord.Color.red()))
            #return

        view: DwiJipGyi = DwiJipGyi(red_team, blue_team, x, y, timelast, money)
        msg = await ctx.send("`뒤집기 준비중...`", view=view)
        view.message = msg
        await view.init()

    @testing.command(name='선택', aliases=['selection'])
    async def selection(self, ctx: commands.Context):
        msg = await ctx.send("Selection", view=Teselect())


def setup(bot):
    bot.add_cog(Testing(bot))

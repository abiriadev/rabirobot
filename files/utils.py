from typing import Union
import discord
from discord.ext import commands


async def send_not_enough_args(ctx, arg_index: int, *args: list[str]):
    command: commands.Command = ctx.command
    arg_text = ""

    i = 0
    for a in args:
        if arg_index == i:
            arg_text += f" **`{a}`**"
        else:
            arg_text += f" `{a}`"
        i += 1

    embed = discord.Embed(
        description=f"매개변수가 충분하지 않습니다.\n`{ctx.prefix}{command.qualified_name}` {arg_text}",
        color=discord.Colour.dark_gray()
    )
    print(arg_text)
    await ctx.send(embed=embed)
    return


commands.Context.send_not_enough_args = send_not_enough_args


def parse_user(guild: discord.Guild, toParse: Union[int, str]):
    try:
        user = int(toParse)
        result = guild.get_member(toParse)
        if result is None:
            return None
    except ValueError:
        result = guild.get_member_named(toParse)
        if result is None:
            try:
                result = guild.get_member(int(toParse[3:-1]))
                if result is None:
                    return
            except ValueError:
                return
    return result

# 일반적인 경우에선 parse_user가 필요하지 않습니다. 매개변수에 user: Union[discord.Member, discord.User, int, str]을 넣는 것으로 해결할 수 있습니다.

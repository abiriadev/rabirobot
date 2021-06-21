from typing import Union
import discord

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
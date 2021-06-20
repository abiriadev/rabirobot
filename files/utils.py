def parseUser(guild, toParse):
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

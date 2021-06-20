
def parseUser(guild, input):
    try:
        user = int(input)
        result = guild.get_member(input)
        if result is None:
            return None
    except ValueError:
        result = guild.get_member_named(input)
        if result is None:
            try:
                result = guild.get_member(int(input[3:-1]))
                if result is None:
                    return
            except ValueError:
                return
    return result
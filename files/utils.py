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

emoji = {
    0: '<:0_:856124552936816670>',
    1: '<:1_:856122825441280060>',
    2: '<:2_:856122824963784705>',
    3: '<:3_:856122824908603403>',
    4: '<:4_:856122825340223528>',
    5: '<:5_:856122825362112522>',
    6: '<:6_:856122825508388884>',
    7: '<:7_:856122825396322345>',
    8: '<:8_:856122825324888074>',
    9: '<:9_:856122825534603294>',
    10: '<:10:856122825411526666>',
    11: '<:11:856122825353199626>',
    12: '<:12:856123293802299402>',
    13: '<:13:856122825327771648> ',
    14: '<:14:856122825403793408> ',
    15: '<:15:856122825387016222> ',
    16: '<:16:856122825017524255> ',
    17: '<:17:856122825361981490> ',
    18: '<:18:856122825399468032> ',
    19: '<:19:856122825449799680> ',
    20: '<:20:856122825437872128>',
}


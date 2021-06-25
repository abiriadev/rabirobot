from discord.ext import commands

bot_token = 'ODU1NjUyODM3MjM2NjcwNDY0.YM1mzQ.2fiCLc8Tlc23ps-IrQ4NVQArCnc'
bot_prefix = 'r/'
bot_owner = [
    726952789770633317, 
    674561377612070936, 
    768277889757347860, 
    536517275667267605, 
    825244975226421248, 
    533260359604109342, 
    662201438621138954
]

debug = True
version = "0.0.1"
identifier = "dev"
build_string: str
build_channel = 857491495305216030
build: int

extensions = [
    'cogs.verify',
    'cogs.chat',
    'cogs.money',
    'cogs.event',
    'cogs.vote',
    'cogs.leveling'
]

if debug:
    extensions.append('cogs.debug')
import asyncio
import time
from typing import *

import discord
from discord.ext import commands

import data.db
import main
from files.emoji import CustomEmoji

class Game(commands.Cog):
    commands.group(name="게임", aliases=['game', 'g', '겜', '미니게임'])
    ...

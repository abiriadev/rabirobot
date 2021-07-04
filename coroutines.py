import asyncio
from typing import Union, Optional

import discord
from discord import Thread
from discord.abc import PrivateChannel
from discord.ext import commands
from discord import guild

from data import db


async def refresh_verification(bot: commands.Bot):
    while True:
        for ukey in db.database.players.keys():
            user = db.database.Player(ukey)
            chnId: Optional[int] = user.vf_message_channel
            msgId = user.vf_message_id

            if (chnId is None) or (msgId is None):
                continue

            print(f"Checking user {ukey}")
            try:
                chn: Union[guild.GuildChannel, PrivateChannel, Thread] = await bot.fetch_channel(chnId)
            except discord.Forbidden:
                user.vf_message_channel = None
                print(f"Channel cannot be accessed")
                return

            if chn is None:
                user.vf_message_channel = None
                print(f"Channel not found")
                
            else:
                try:
                    await chn.fetch_message(msgId)
                except discord.DiscordException:
                    user.vf_message_id = None
                    print(f"Message not found")

        await asyncio.sleep(5 * 60)

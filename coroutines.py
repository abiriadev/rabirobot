import asyncio

import discord
from discord.ext import commands

from data import db


async def refresh_verification(bot: commands.Bot):
    while True:
        for ukey in db.database.players.keys():
            user = db.database.Player(ukey)
            chnId = user.vf_message_channel
            msgId = user.vf_message_id

            if (chnId is None) or (msgId is None):
                continue

            print(f"Checking user {ukey}")

            chn: discord.TextChannel = await bot.fetch_channel(chnId)

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

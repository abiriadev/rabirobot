import asyncio
import discord


class PlayerData:
    _selfDict: dict
    _id: int

    @property
    def id(self):
        return self._id

    @property
    def level(self):
        return self._selfDict["level"]

    @property
    def money(self):
        return self._selfDict["money"]

    @property
    def vf_message_channel(self):
        return self._selfDict["vf_message_channel"]

    @property
    def vf_message_id(self):
        return self._selfDict["vf_message_id"]

    @property
    def verified(self):
        return self.vf_message_id is not None

    @level.setter
    def level(self, level: int):
        self._selfDict["level"] = level

    @money.setter
    def money(self, money: int):
        self._selfDict["money"] = money

    @vf_message_channel.setter
    def vf_message_channel(self, chnid: int):
        self._selfDict["vf_message_channel"] = chnid

    @vf_message_id.setter
    def vf_message_id(self, chnid: int):
        self._selfDict["vf_message_id"] = chnid

    def __init__(self, id: int, selfDict: dict):
        self._id = id
        self._selfDict = selfDict
        if "money" not in self._selfDict:
            self._selfDict["money"] = 0

        if "level" not in self._selfDict:
            self._selfDict["level"] = 0

        if "vf_message_channel" not in self._selfDict:
            self._selfDict["vf_message_channel"] = None

        if "vf_message_id" not in self._selfDict:
            self._selfDict["vf_message_id"] = None

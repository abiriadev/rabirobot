
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

    @level.setter
    def level(self, level: int):
        self._selfDict["level"] = level

    @money.setter
    def money(self, money: int):
        self._selfDict["money"] = money

    def __init__(self, id: int, selfDict: dict):
        self._id = id
        self._selfDict = selfDict
        if "money" not in self._selfDict:
            self._selfDict["money"] = 0

        if "level" not in self._selfDict:
            self._selfDict["level"] = 0

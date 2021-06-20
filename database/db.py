import yaml


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


class Players:
    players: dict

    def __init__(self):
        self.players = {}

    def __getitem__(self, item: int):
        if self.players == None:
            self.players = {}
        if item not in self.players.keys():
            self.players[item] = {}
        self.save()
        return PlayerData(item, self.players[item])

    def __iter__(self):
        return self.players.__iter__()

    def save(self):
        yaml.dump(self.__dict__, open("./files/data.yml", mode='w', encoding='utf-8'), sort_keys=True)

    @staticmethod
    def load():
        players = yaml.load(open("./files/data.yml", mode='r', encoding='utf-8'), Loader=yaml.FullLoader)
        result = Players()
        if players is not None and 'players' in players.keys():
            result.players = players['players']
        return result


players = Players.load()

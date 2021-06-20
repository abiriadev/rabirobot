import yaml

from database.player import PlayerData


class Data:
    players: dict
    votes: dict

    def __init__(self):
        self.players = {}
        self.votes = {}

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
        data = yaml.load(open("./files/data.yml", mode='r', encoding='utf-8'), Loader=yaml.FullLoader)
        result = Data()
        if data is not None:
            if 'players' in data.keys():
                result.players = data['players']

            if 'votes' in data.keys():
                result.votes = data['votes']
        return result


players = Data.load()

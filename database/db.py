import yaml

from database.player import PlayerData
from database.vote import VoteData


class Data:
    players: dict
    votes: dict

    def __init__(self):
        self.players = {}
        self.votes = {}

    def Player(self, item: int):
        if self.players is None:
            self.players = {}
        if item not in self.players.keys():
            self.players[item] = {}
        self.save()
        return PlayerData(item, self.players[item])

    def Vote(self, channel: int):
        if self.votes is None:
            self.votes = {}
        if channel not in self.votes.keys():
            self.votes[channel] = {}
        self.save()
        return VoteData(channel, self.votes[channel])


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

        if result.players is None:
            result.players = {}

        if result.votes is None:
            result.votes = {}
        return result


database = Data.load()

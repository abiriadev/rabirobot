
class VoteData:
    _selfDict: dict

    @property
    def title(self):
        return self._selfDict["title"]

    @property
    def description(self):
        return self._selfDict["description"]

    @property
    def fields(self):
        return self._selfDict["fields"]

    @title.setter
    def title(self, title: int):
        self._selfDict["title"] = title

    @description.setter
    def description(self, description: int):
        self._selfDict["description"] = description

    @fields.setter
    def fields(self, fields: int):
        self._selfDict["fields"] = fields

    def __init__(self, id: int, selfDict: dict):
        self._id = id
        self._selfDict = selfDict
        if "title" not in self._selfDict:
            self._selfDict["title"] = 0

        if "description" not in self._selfDict:
            self._selfDict["description"] = 0

        if "fields" not in self._selfDict:
            self._selfDict["fields"] = 0

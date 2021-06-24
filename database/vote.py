import discord
from files.emoji import numbers

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

    @property
    def published(self):
        return self._selfDict["published"]

    @property
    def messageId(self):
        return self._selfDict["messageId"]

    @property
    def additionalMessages(self):
        return self._selfDict["additionalMessages"]

    @property
    def embed(self):
        result = discord.Embed(title=self.title, description=self.description)
        fields: dict = self.fields
        i = 1
        result.description += "\n\n"
        for k in fields:
            result.description += f"**[{i}]**  {k}\n"
            i += 1
        return result

    @property
    def preview(self):
        result: discord.Embed = self.embed
        result._colour = discord.Colour.darker_gray()
        result.set_footer(text="<Vote Preview>")
        return result

    @title.setter
    def title(self, title: int):
        self._selfDict["title"] = title

    @description.setter
    def description(self, description: int):
        self._selfDict["description"] = description

    @fields.setter
    def fields(self, fields: int):
        self._selfDict["fields"] = fields

    @published.setter
    def published(self, published: bool):
        self._selfDict["published"] = published

    @messageId.setter
    def messageId(self, mid: int):
        self._selfDict["messageId"] = mid

    @additionalMessages.setter
    def additionalMessages(self, msgs: list[int]):
        self._selfDict["additionalMessages"] = msgs

    def __init__(self, id: int, selfDict: dict):
        self._id = id
        self._selfDict = selfDict
        if "title" not in self._selfDict:
            self._selfDict["title"] = "Title placeholder"

        if "description" not in self._selfDict:
            self._selfDict["description"] = "Description placeholder"

        if "fields" not in self._selfDict:
            self._selfDict["fields"] = []

        if "published" not in self._selfDict:
            self._selfDict["published"] = False

        if "messageId" not in self._selfDict:
            self._selfDict["messageId"] = None

        if "additionalMessages" not in self._selfDict:
            self._selfDict["additionalMessages"] = []

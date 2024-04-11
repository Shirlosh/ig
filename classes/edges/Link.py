from classes.edges.Edge import Edge
from classes.vertices.Site import Site


class Link(Edge):
    def __init__(self, site1: Site, site2: Site, *, ID=None):
        super().__init__(site1, site2, ID=ID)
        self.__channels = {}

    @property
    def Channels(self):
        return self.__channels

    def Channel(self, channelID):
        return self.__channels.get(channelID, None)

    def AddChannel(self, channel: Channel):
        self.__channels[channel.ID] = channel
        return channel

    def RemoveChannel(self, channelID):
        return self.__channels.pop(channelID, None)

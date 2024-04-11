from classes.edges.Channel import Channel
from classes.edges.Interference import Interference
from modules.data.dictionaries import ListDictionaryValues


def NetworkClass(topology, *topologyArgs, **topologyKWArgs):

    class Network(topology):
        def __init__(self):
            """
            Returns a class Network which forces the topology @topology.
            Note that we do not support multigraph for Networks. Links are singular between any two sites.
            Links can contain multiple channels though.
            """
            topologyKWArgs['multigraph'] = False
            super().__init__(*topologyArgs, **topologyKWArgs)

        @property
        def Channels(self) -> list[Channel]:
            """
            :return: each channel of every link in the network.
            """
            return [channel for link in self.Edges.values() for channel in link.Channels.values()]

        @property
        def Interferences(self, *, asMap=False, includeSelfInterference=False):
            """
            Returns all interference between links in the network
            :param asMap: Changes type of output to map
            :param includeSelfInterference: will include interference between a link and itself
            :return: list[Interference] if asMap else {Link.ID: {Link.ID: Interference}}
            """
            interferences = {}
            for sourceLink in self.Links:
                interferences[sourceLink.ID] = {}
                for targetLink in self.Links:
                    if not includeSelfInterference and sourceLink.ID == targetLink.ID: continue
                    interferences[sourceLink.ID][targetLink.ID] = self.InterferenceFromOn(sourceLink.ID, targetLink.ID)
            return interferences if asMap else ListDictionaryValues(interferences)

        @property
        def Links(self):
            return self.Edges

        def Link(self, linkID):
            return self.Edge(linkID)

        def Channel(self, linkID, channelID):
            link = self.Link(linkID)
            return link.Channel(channelID) if link else None

        def InterferenceFrom(self, linkID, *, includeSelfInterference=False):
            """
            Returns all interference from a link with ID linkID to all links in the network
            :param linkID: The ID of the required link
            :param includeSelfInterference: will include interference between the link and itself
            :return: list[Interference]
            """
            if not self.Link(linkID): return None
            interferences = []
            [interferences.extend(self.InterferenceFromOn(linkID, link.ID)) for link in self.Links
             if includeSelfInterference or linkID != link.ID]
            return interferences

        def InterferenceOn(self, linkID, *, includeSelfInterference=False):
            """
            Returns all interference from all links in the network to a link with ID linkID
            :param linkID: The ID of the required link
            :param includeSelfInterference: will include interference between the link and itself
            :return: list[Interference]
            """
            if not self.Link(linkID): return None
            interferences = []
            [interferences.extend(self.InterferenceFromOn(link.ID, linkID)) for link in self.Links
             if includeSelfInterference or linkID != link.ID]
            return interferences

        def InterferenceFromOn(self, linkID1, linkID2):
            link1, link2 = self.Link(linkID1), self.Link(linkID2)
            return [Interference(sourceChannel, targetChannel) for sourceChannel in link1.Channels for targetChannel in link2.Channels]

        def InterferenceBetween(self, linkID1, linkID2):
            interferences = self.InterferenceFromOn(linkID1, linkID2)
            if interferences: interferences.extend(self.InterferenceFromOn(linkID2, linkID1))
            return interferences

        def GetLinkBetween(self, site1ID, site2ID):
            return self.GetBetween(site1ID, site2ID)

        @property
        def Sites(self):
            return self.Vertices

        def Site(self, siteID):
            return self.Vertex(siteID)

        def AddSite(self, site: Site = None, **kwargs):
            return self.AddVertex(site, **kwargs)

        def AddVertex(self, vertex: Site = None, **kwargs):
            super().AddVertex(vertex, **kwargs)

        def RemoveSite(self, siteID):
            return self.RemoveVertex(siteID)

        def RemoveVertex(self, vertexID):
            return super().RemoveVertex(vertexID)

        def AddLink(self, link: Link, **kwargs):
            return self.AddEdge(link, **kwargs)

        def RemoveLink(self, linkID):
            return self.RemoveEdge(linkID)

    return Network

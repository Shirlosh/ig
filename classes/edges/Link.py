from classes.edges.DirectedEdge import DirectedEdge
from classes.vertices.Site import Site
from modules.mathematics.Geometry import GlobeDistance
from modules.mathematics.RF import FSPL, AttenuatedLevel, ChannelNoise

defaults = {  # defaults are for 1ft antenna, frequency 15Ghz and a common bandwidth profile
    'frequency': 15,  # in Ghz
    'bandwidth': 28,  # in Mb
    'TxLevel': 18,  # in DB
    'TxGain': 32,  # in DB
    'RxGain': 32  # in DB
}


class Link(DirectedEdge):
    def __init__(self, v1: Site, v2: Site, *, frequency=defaults['frequency'],
                                             bandwidth=defaults['bandwidth'],
                                             TxLevel=defaults['TxLevel'],
                                             TxGain=defaults['TxGain'],
                                             RxGain=defaults['RxGain'], ID=None):
        super().__init__(v1, v2, ID=ID)
        self.__frequency = frequency
        self.__bandwidth = bandwidth
        self.__TxLevel = TxLevel
        self.__TxGain = TxGain
        self.__RxGain = RxGain

    @property
    def Frequency(self):
        return self.__frequency

    @Frequency.setter
    def Frequency(self, frequency):
        self.__frequency = frequency

    @property
    def TxLevel(self):
        return self.__TxLevel

    @TxLevel.setter
    def TxLevel(self, level):
        self.__TxLevel = level

    @property
    def TxGain(self):
        return self.__TxGain

    @TxGain.setter
    def TxGain(self, gain):
        self.__TxGain = gain

    @property
    def RxGain(self):
        return self.__RxGain

    @RxGain.setter
    def RxGain(self, gain):
        self.__RxGain = gain

    @property
    def Distance(self):
        return GlobeDistance(self.Source.Location, self.Target.Location)

    @property
    def FSPL(self):
        return FSPL(self.__frequency, self.__TxGain, self.__RxGain, self.Distance)

    @property
    def AttenuatedLevel(self):
        return AttenuatedLevel(self.__TxLevel, self.__TxGain, self.__RxGain, self.__frequency, self.Distance, 0, 0)

    @property
    def ChannelNoise(self):
        return ChannelNoise(self.__bandwidth)



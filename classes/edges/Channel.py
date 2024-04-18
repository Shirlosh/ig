from classes.abstracts.Mappable import Mappable
from classes.edges.Edge import Edge
from modules.mathematics.Geometry import GlobeDistance
from modules.mathematics.RF import FSPL, AttenuatedLevel, ChannelNoise

defaults = {  # defaults are for 1ft antenna, frequency 15Ghz and a common bandwidth profile
    'frequency': 15,  # in Ghz
    'bandwidth': 28,  # in Mb
    'TxLevel': 18,  # in DB
    'TxGain': 32,  # in DB
    'RxGain': 32  # in DB
}


class Channel(Edge, Mappable):
    def __init__(self, link, *, frequency=defaults['frequency'],
                                      bandwidth=defaults['bandwidth'],
                                      TxLevel=defaults['TxLevel'],
                                      TxGain=defaults['TxGain'],
                                      RxGain=defaults['RxGain'],
                                      ID=None):
        super().__init__(link.Source, link.Target, ID=ID)
        self.__frequency = frequency
        self.__bandwidth = bandwidth
        self.__TxLevel = TxLevel
        self.__TxGain = TxGain
        self.__RxGain = RxGain
        self.__link = link

    @property
    def Link(self):
        return self.__link

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
    def RxLevel(self):
        return AttenuatedLevel(self.__TxLevel, self.__TxGain, self.__RxGain, self.__frequency, self.Distance, 0, 0)

    @property
    def ChannelNoise(self):
        return ChannelNoise(self.__bandwidth)

    @property
    def Vector(self):
        sLoc, tLoc = self.Source.Location, self.Target.Location
        return tLoc[0] - sLoc[0], tLoc[1] - sLoc[1]

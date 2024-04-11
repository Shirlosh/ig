from classes.edges.Channel import Channel
from classes.edges.Edge import Edge
from modules.mathematics.Geometry import GlobeDistance, AngleBetweenVectors, ReverseVector
from modules.mathematics.RF import RPF, FSPL, AttenuatedLevel


class Interference(Edge):
    def __init__(self, originChannel: Channel, interferedChannel: Channel, *, ID=None):
        super().__init__(originChannel.Source, interferedChannel.Target, ID=ID)
        self.__originChannel = originChannel
        self.__interferedChannel = interferedChannel
        self.__transmissionAngle = AngleBetweenVectors(self.__originChannel.Vector, self.Vector)
        self.__arrivalAngle = AngleBetweenVectors(ReverseVector(self.__interferedChannel.Vector), ReverseVector(self.Vector))

    @property
    def originChannel(self):
        return self.__originChannel

    @property
    def interferedChannel(self):
        return self.__interferedChannel

    @property
    def TransmissionAngle(self):
        return self.__transmissionAngle

    @property
    def ArrivalAngle(self):
        return self.__arrivalAngle

    @property
    def Frequency(self):
        return self.__originChannel.Frequency

    @property
    def TxLevel(self):
        return self.__originChannel.TxLevel

    @property
    def TxGain(self):
        return RPF(self.__originChannel.TxGain, self.__transmissionAngle)

    @property
    def RxGain(self):
        return RPF(self.__interferedChannel.RxGain, self.__arrivalAngle)

    @property
    def Distance(self):
        return GlobeDistance(self.Source.Location, self.Target.Location)

    @property
    def FSPL(self):
        return FSPL(self.Frequency, self.TxGain, self.RxGain, self.Distance)

    @property
    def RxLevel(self):
        return AttenuatedLevel(self.TxLevel, self.TxGain, self.RxGain, self.Frequency, self.Distance, 0, 0)

    @property
    def Vector(self):
        sLoc, tLoc = self.Source.Location, self.Target.Location
        return tLoc[0] - sLoc[0], tLoc[1] - sLoc[1]

import math
from scipy.constants import Boltzmann as boltzmann


def DBtoMW(db):
    return 10 ** (db / 10)


def MWtoDB(mw):
    return math.log10(mw) * 10


def RPF(gain, angle, *, separationAngle: float = 90, beamWidth: float = 1.0):
    """
    :param gain: the initial gain of the signal in DB
    :param angle: the angle compared to the signal direction
    :param separationAngle: optional, the angle where the signal strength is considered a flat 0
    :param beamWidth: optional, the beam width of the antenna. Default is 1.0
    :return: gain, in DB, at the angle, according to an RPF of a common 1ft antenna
    """
    inMW = DBtoMW(gain) / math.exp((4 / math.sqrt(2)) * ((angle / beamWidth) ** 2)) if abs(angle) < separationAngle else 0
    return MWtoDB(inMW)


def ReverseRPF(gain, angle, *, beamWidth: float = 1.0):
    """
    :param gain: a target gain of a signal in DB
    :param angle: the angle compared to the signal direction
    :param beamWidth: optional, the beam width of the antenna. Default is 1.0
    :return: gain, in DB, at angle 0, according to an RPF of a common 1ft antenna
    """
    inMW = DBtoMW(gain) * math.exp((4 / math.sqrt(2)) * ((angle / beamWidth) ** 2))
    return MWtoDB(inMW)


def FSPL(frequency, TxGain, RxGain, distance):
    """
    :param frequency: in Ghz
    :param TxGain: in DB
    :param RxGain: in DB
    :param distance: in kilometers
    :return: the Free Space Path Loss in DB
    """
    return 20 * (math.log10(distance * frequency)) + 92.45 - TxGain - RxGain


def AttenuatedLevel(TxLevel, TxGain, RxGain, frequency, distance, angleOfTransmission, angleOfArrival, *, separationAngle: float = 90, beamWidth: float = 1.0):
    rpf = lambda g, a: RPF(g, a, separationAngle=separationAngle, beamWidth=beamWidth)
    return TxLevel - FSPL(frequency, rpf(TxGain, angleOfTransmission), rpf(RxGain, angleOfArrival), distance)


def ReverseAttenuatedLevel(RxLevel, TxGain, RxGain, frequency, distance, angleOfTransmission, angleOfArrival, *, beamWidth: float = 1.0):
    rpf = lambda g, a: ReverseRPF(g, a, beamWidth=beamWidth)
    return RxLevel + FSPL(frequency, rpf(TxGain, angleOfTransmission), rpf(RxGain, angleOfArrival), distance)


def ChannelNoise(bandwidth, *, temperature: float = 25.0):
    """
    :param bandwidth: bandwidth of a channel
    :param temperature: Environmental temperature
    :return: the thermal noise of the channel in DB
    """
    return boltzmann * temperature * bandwidth


def SINR(TxLevel, interferenceLevel, bandwidth):
    return TxLevel - interferenceLevel - ChannelNoise(bandwidth)


def Capacity(SINRvalue, bandwidth):
    """
    :param SINRvalue: Signal-Interference-Noise-Ratio
    :param bandwidth: of the channel
    :return: capacity of the channel
    """
    return bandwidth * math.log2(1 + SINRvalue)

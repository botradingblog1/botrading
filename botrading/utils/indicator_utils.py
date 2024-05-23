from ..strategy_builder.indicator import Indicator
from ..enums import IndicatorType


def SMA(timeperiod=200):
    return Indicator(name=IndicatorType.SMA, params={'timeperiod': timeperiod})

def EMA(timeperiod=3):
    return Indicator(name=IndicatorType.EMA, params={'timeperiod': timeperiod})

def DM(timeperiod=14):
    return Indicator(name=IndicatorType.DM, params={'timeperiod': timeperiod})

def FisherTransform(length=9):
    return Indicator(name=IndicatorType.FISHER_TRANSFORM, params={'length': length})

def WilliamsR(timeperiod=14):
    return Indicator(name=IndicatorType.WILLIAMSR, params={'timeperiod': timeperiod})

def RSI(timeperiod=14):
    return Indicator(name=IndicatorType.RSI, params={'timeperiod': timeperiod})

def MACD(fastperiod=12, slowperiod=26, signalperiod=9):
    return Indicator(name=IndicatorType.MACD, params={'fastperiod': fastperiod, 'slowperiod': slowperiod, 'signalperiod': signalperiod})

def BBANDS(timeperiod=20, nbdevup=2, nbdevdn=2):
    return Indicator(name=IndicatorType.BBANDS, params={'timeperiod': timeperiod, 'nbdevup': nbdevup, 'nbdevdn': nbdevdn})

def ATR(timeperiod=14):
    return Indicator(name=IndicatorType.ATR, params={'timeperiod': timeperiod})

def OBV():
    return Indicator(name=IndicatorType.OBV, params={})

def LAG(period=1):
    return Indicator(name=IndicatorType.LAG, params={'period': period})

def DELTA(period=1):
    return Indicator(name=IndicatorType.DELTA, params={'period': period})


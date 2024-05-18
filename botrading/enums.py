from enum import Enum


class MarketIndex(Enum):
    """
    List of common market indexes like NASDAQ 100, Dow Jones or S&P 500
    """
    NASDAQ_100 = 'NASDAQ_100'
    SNP_500 = 'SNP_500'
    DJI = 'DJI'
    RUSSELL_1000 = 'RUSSELL_1000'
    RUSSELL_2000 = 'RUSSELL_2000'


class Position(Enum):
    """
    Position enum like 'long' or 'short'
    """
    LONG = 'LONG'
    SHORT = 'SHORT'
    UNKNOWN = 'UNKNOWN'


class Side(Enum):
    """
    Order side like 'buy' or 'sell'
    """
    BUY = 'BUY'
    SELL = 'SELL'
    UNKNOWN = 'UNKNOWN'


class Exchange(Enum):
    """
    Enum for different stock exchanges.
    """
    NYSE = 'NYSE'
    NASDAQ = 'NASDAQ'
    CME = 'CME'
    LSE = 'LSE'


class TimeZone(Enum):
    """
    Enum for different time zones.
    """
    US_EASTERN = 'America/New_York'
    US_CENTRAL = 'America/Chicago'
    US_PACIFIC = 'America/Los_Angeles'
    LONDON = 'Europe/London'
    UTC = 'UTC'


class TiingoInterval(Enum):
    """
    Enum for different Tiingo resample intervals.
    """
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'


class YahooInterval(Enum):
    """
    Enum for different Yahoo data intervals.
    """
    ONE_MINUTE = '1m'
    TWO_MINUTES = '2m'
    FIVE_MINUTES = '5m'
    FIFTEEN_MINUTES = '15m'
    THIRTY_MINUTES = '30m'
    SIXTY_MINUTES = '60m'
    NINETY_MINUTES = '90m'
    ONE_HOUR = '1h'
    ONE_DAY = '1d'
    FIVE_DAYS = '5d'
    ONE_WEEK = '1wk'
    ONE_MONTH = '1mo'
    THREE_MONTHS = '3mo'


class YahooPeriod(Enum):
    """
    Enum for different Yahoo data periods.
    """
    ONE_DAY = '1d'
    FIVE_DAYS = '5d'
    ONE_MONTH = '1mo'
    THREE_MONTHS = '3mo'
    SIX_MONTHS = '6mo'
    ONE_YEAR = '1y'
    TWO_YEARS = '2y'
    FIVE_YEARS = '5y'
    TEN_YEARS = '10y'
    YEAR_TO_DATE = 'ytd'
    MAX = 'max'

class DataType(Enum):
    """
    Enum for different data types.
    """
    STOCKS = 'STOCKS'
    CRYPTO = 'CRYPTO'
    NEWS = 'NEWS'
    FOREX = 'FOREX'



from enum import Enum


class OrderStatus(Enum):
    NEW = "new"
    ACCEPTED = "accepted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    DONE_FOR_DAY = "done_for_day"
    CANCELED = "canceled"
    EXPIRED = "expired"
    REPLACED = "replaced"
    PENDING_CANCEL = "pending_cancel"
    PENDING_REPLACE = "pending_replace"
    PENDING_REVIEW = "pending_review"
    PENDING_NEW = "pending_new"
    ACCEPTED_FOR_BIDDING = "accepted_for_bidding"
    STOPPED = "stopped"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
    CALCULATED = "calculated"
    HELD = "held"


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"


class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"


class TimeInForce(Enum):
    GTC = "gtc"
    DAY = "day"
    OPG = "opg"
    CLS = "cls"
    IOC = "ioc"
    FOK = "fok"


class TimeInterval(Enum):
    DAY = 'DAY'
    HOUR = 'HOUR'
    MINUTE = 'MINUTE'
    SECOND = 'SECOND'
    MILLIS = 'MILLIS'


class MarketIndex(Enum):
    """
    List of common market indexes like NASDAQ 100, Dow Jones or S&P 500
    """
    NASDAQ_100 = 'NASDAQ_100'
    SNP_500 = 'SNP_500'
    DJI = 'DJI'
    RUSSELL_1000 = 'RUSSELL_1000'
    RUSSELL_2000 = 'RUSSELL_2000'
    UNKNOWN = 'UNKNOWN'


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
    UNKNOWN = 'UNKNOWN'


class TimeZone(Enum):
    """
    Enum for different time zones.
    """
    US_EASTERN = 'America/New_York'
    US_CENTRAL = 'America/Chicago'
    US_PACIFIC = 'America/Los_Angeles'
    LONDON = 'Europe/London'
    UTC = 'UTC'
    UNKNOWN = 'UNKNOWN'


class TiingoIntradayInterval(Enum):
    """
    Enum for different Tiingo intraday resample intervals.
    """
    MIN_1 = '1min'
    MIN_5 = '5min'
    MIN_15 = '15min'
    MIN_30 = '30min'
    HOUR_1 = '1hour'
    HOUR_4 = '4hour'
    DAY_1 = '1day'

class TiingoDailyInterval(Enum):
    """
    Enum for different daily Tiingo resample intervals.
    """
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTYLY = 'monthly'
    ANNUALLY = 'annually'

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
    UNKNOWN = 'UNKNOWN'


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
    UNKNOWN = 'UNKNOWN'

class DataType(Enum):
    """
    Enum for different data types.
    """
    STOCKS = 'STOCKS'
    CRYPTO = 'CRYPTO'
    NEWS = 'NEWS'
    FOREX = 'FOREX'
    ECONOMIC = 'ECONOMIC'
    UNKNOWN = 'UNKNOWN'


class EconomicIndicators(Enum):
    """
    Enum for most economic indicators that may affect stock prices.
    """
    TEN_YEAR_TREASURY_YIELD = 'DGS10'
    TWO_YEAR_TREASURY_YIELD = 'DGS2'
    UNEMPLOYMENT_RATE = 'UNRATE'
    GDP = 'GDPC1'
    CPI = 'CPIAUCSL'
    CONSUMER_CONFIDENCE = 'CSCICP03USM665S'
    NON_FARM_PAYROLL = 'PAYEMS'
    RETAIL_FOOD_SALES = 'MRTSSM44X72USS'
    PRODUCER_PRICE_INDEX = 'PPIACO'
    INDUSTRIAL_PRODUCTION_INDEX = 'INDPRO'
    VIX = 'VIXCLS'
    SP500 = 'SP500'
    UNIVERSITY_MICHIGAN_CONSUMER_SENTIMENT = 'UMCSENT'
    OECD_RECESSION_INDEX = 'USARECM'
    FRED_NATIONAL_FINANCIAL_CONDITION_INDEX = 'NFCI'
    ICE_BOFA_US_HIGH_HIELD_INDEX = 'BAMLHYH0A0HYM2TRIV'
    FRED_FINANCIAL_STRESS_INDEX = 'STLFSI4'
    TEN_YEAR_BREAKEVEN_INFLATTION_RATE = 'T10YIE'
    UNKNOWN = 'UNKNOWN'


class StrategyOperator(Enum):
    LOWER_THAN = "LOWER_THAN"
    GREATER_THAN = "GREATER_THAN"
    CROSS_FROM_BELOW = "CROSS_FROM_BELOW"
    CROSS_FROM_ABOVE = "CROSS_FROM_ABOVE"
    UNKNOWN = 'UNKNOWN'


class RiskManagementType(Enum):
    STOP_LOSS = 'STOP_LOSS'
    TRAILING_STOP = 'TRAILING_STOP'
    TAKE_PROFIT = 'TAKE_PROFIT'
    UNKNOWN = 'UNKNOWN'


class Theme(Enum):
    LIGHT_THEME = 'LIGHT_THEME'
    DARK_THEME = 'DARK_THEME'
    UNKNOWN = 'UNKNOWN'


class StatsMethod(Enum):
    PEARSON_CORRELATION = 'PEARSON_CORRELATION'
    MUTUAL_INFORMATION = 'MUTUAL_INFORMATION'
    RANDOM_FOREST_INFORMATION = 'RANDOM_FOREST_INFORMATION'
    UNKNOWN = 'UNKNOWN'



class IndicatorCategory(str, Enum):
    MOMENTUM = 'MOMENTUM'
    VOLATILITY = 'VOLATILITY'
    TREND = 'TREND'
    VOLUME = 'VOLUME'


class IndicatorType(str, Enum):
    SMA = 'SMA'
    EMA = 'EMA'
    BBANDS = 'BBANDS'
    BBANDS_LOWER = 'BBANDS_LOWER'
    BBANDS_MIDDLE = 'BBANDS_MIDDLE'
    BBANDS_UPPER = 'BBANDS_UPPER'
    ATR = 'ATR'
    AO = 'AO'
    APO = 'APO'
    MACD = 'MACD'
    RSI = 'RSI'
    BOP = 'BOP'
    CCI = 'CCI'
    CMO = 'CMO'
    DM = 'DM'
    MOM = 'MOM'
    PPO = 'PPO'
    ROC = 'ROC'
    TRIX = 'TRIX'
    UO = 'UO'
    WILLIAMSR = 'WILLIAMSR'
    FISHER_TRANSFORM = 'FISHER_TRANSFORM'
    ADX = 'ADX'
    AROON = 'AROON'
    PSAR = 'PSAR'
    LOW_BBAND = 'LOW_BBAND'
    HIGH_BBAND = 'HIGH_BBAND'
    LOW_DONCHIAN = 'LOW_DONCHIAN'
    HIGH_DONCHIAN = 'HIGH_DONCHIAN'
    LOW_KC = 'LOW_KC'
    HIGH_KC = 'HIGH_KC'
    AD = 'AD'
    OBV = 'OBV'
    CMF = 'CMF'
    MFI = 'MFI'
    LAG = 'LAG'
    DELTA = 'DELTA'


class CandlestickPattern(Enum):
    """
    TA-Lib's candle patterns
    """
    CDL2CROWS = 'CDL2CROWS'
    CDL3BLACKCROWS = 'CDL3BLACKCROWS'
    CDL3INSIDE = 'CDL3INSIDE'
    CDL3LINESTRIKE = 'CDL3LINESTRIKE'
    CDL3OUTSIDE = 'CDL3OUTSIDE'
    CDL3STARSINSOUTH = 'CDL3STARSINSOUTH'
    CDL3WHITESOLDIERS = 'CDL3WHITESOLDIERS'
    CDLABANDONEDBABY = 'CDLABANDONEDBABY'
    CDLADVANCEBLOCK = 'CDLADVANCEBLOCK'
    CDLBELTHOLD = 'CDLBELTHOLD'
    CDLBREAKAWAY = 'CDLBREAKAWAY'
    CDLCLOSINGMARUBOZU = 'CDLCLOSINGMARUBOZU'
    CDLCONCEALBABYSWALL = 'CDLCONCEALBABYSWALL'
    CDLCOUNTERATTACK = 'CDLCOUNTERATTACK'
    CDLDARKCLOUDCOVER = 'CDLDARKCLOUDCOVER'
    CDLDOJI = 'CDLDOJI'
    CDLDOJISTAR = 'CDLDOJISTAR'
    CDLDRAGONFLYDOJI = 'CDLDRAGONFLYDOJI'
    CDLENGULFING = 'CDLENGULFING'
    CDLEVENINGDOJISTAR = 'CDLEVENINGDOJISTAR'
    CDLEVENINGSTAR = 'CDLEVENINGSTAR'
    CDLGAPSIDESIDEWHITE = 'CDLGAPSIDESIDEWHITE'
    CDLGRAVESTONEDOJI = 'CDLGRAVESTONEDOJI'
    CDLHAMMER = 'CDLHAMMER'
    CDLHANGINGMAN = 'CDLHANGINGMAN'
    CDLHARAMI = 'CDLHARAMI'
    CDLHARAMICROSS = 'CDLHARAMICROSS'
    CDLHIGHWAVE = 'CDLHIGHWAVE'
    CDLHIKKAKE = 'CDLHIKKAKE'
    CDLHIKKAKEMOD = 'CDLHIKKAKEMOD'
    CDLHOMINGPIGEON = 'CDLHOMINGPIGEON'
    CDLIDENTICAL3CROWS = 'CDLIDENTICAL3CROWS'
    CDLINNECK = 'CDLINNECK'
    CDLINVERTEDHAMMER = 'CDLINVERTEDHAMMER'
    CDLKICKING = 'CDLKICKING'
    CDLKICKINGBYLENGTH = 'CDLKICKINGBYLENGTH'
    CDLLADDERBOTTOM = 'CDLLADDERBOTTOM'
    CDLLONGLEGGEDDOJI = 'CDLLONGLEGGEDDOJI'
    CDLLONGLINE = 'CDLLONGLINE'
    CDLMARUBOZU = 'CDLMARUBOZU'
    CDLMATCHINGLOW = 'CDLMATCHINGLOW'
    CDLMATHOLD = 'CDLMATHOLD'
    CDLMORNINGDOJISTAR = 'CDLMORNINGDOJISTAR'
    CDLMORNINGSTAR = 'CDLMORNINGSTAR'
    CDLONNECK = 'CDLONNECK'
    CDLPIERCING = 'CDLPIERCING'
    CDLRICKSHAWMAN = 'CDLRICKSHAWMAN'
    CDLRISEFALL3METHODS = 'CDLRISEFALL3METHODS'
    CDLSEPARATINGLINES = 'CDLSEPARATINGLINES'
    CDLSHOOTINGSTAR = 'CDLSHOOTINGSTAR'
    CDLSHORTLINE = 'CDLSHORTLINE'
    CDLSPINNINGTOP = 'CDLSPINNINGTOP'
    CDLSTALLEDPATTERN = 'CDLSTALLEDPATTERN'
    CDLSTICKSANDWICH = 'CDLSTICKSANDWICH'
    CDLTAKURI = 'CDLTAKURI'
    CDLTASUKIGAP = 'CDLTASUKIGAP'
    CDLTHRUSTING = 'CDLTHRUSTING'
    CDLTRISTAR = 'CDLTRISTAR'
    CDLUNIQUE3RIVER = 'CDLUNIQUE3RIVER'
    CDLUPSIDEGAP2CROWS = 'CDLUPSIDEGAP2CROWS'
    CDLXSIDEGAP3METHODS = 'CDLXSIDEGAP3METHODS'

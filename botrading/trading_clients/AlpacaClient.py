from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.models import Order


class AlpacaClient:
    """
    AlpacaClient provides methods to interact with the Alpaca API for both trading and historical data.

    Attributes:
        trading_client (TradingClient): Client for interacting with Alpaca trading endpoints.
        data_client (StockHistoricalDataClient): Client for interacting with Alpaca historical data endpoints.
    """

    def __init__(self, api_key: str, api_secret: str, is_paper_trading: bool = True):
        """
        Initializes the AlpacaClient with the given configuration.

        Parameters:
            cfg (Config): Configuration object containing Alpaca API credentials and settings.
        """
        self.trading_client = TradingClient(api_key, api_secret, paper=is_paper_trading)
        self.data_client = StockHistoricalDataClient(api_key, api_secret)

    def fetch_quote(self, symbol: str):
        """
        Get the latest quote for a given symbol.

        Parameters:
            symbol (str): The stock symbol to fetch the latest quote for.

        Returns:
            dict: The latest quote data for the given symbol.
        """
        try:
            request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            latest_quote = self.data_client.get_stock_latest_quote(request)
            if not latest_quote:
                print(f"No quote data available for {symbol}")
                return None
            quote = latest_quote[symbol]
            return quote
        except Exception as e:
            print(f"Exception in fetch_latest_quote method for {symbol}: {str(e)}")
            return None

    def get_clock(self):
        """
        Get the current market clock.

        Returns:
            Clock: The current market clock.
        """
        return self.trading_client.get_clock()

    def get_positions(self) -> list:
        """
        Get all current positions.

        Returns:
            list: A list of all current positions.
        """
        positions = self.trading_client.get_all_positions()
        return positions

    def get_account(self) -> dict:
        """
        Get account information.

        Returns:
            dict: The account information.
        """
        account = self.trading_client.get_account()
        return account

    def get_available_cash(self) -> float:
        """
        Get the available cash in the account.

        Returns:
            float: The available cash.
        """
        account = self.trading_client.get_account()
        available_cash = account.cash
        return available_cash

    def submit_limit_order(self, request: LimitOrderRequest) -> Order:
        """
        Submit a limit order.

        Parameters:
            request (LimitOrderRequest): The limit order request.

        Returns:
            Order: The submitted order.
        """
        order = self.trading_client.submit_order(request)
        return order

    def submit_market_order(self, symbol: str, qty: int, side: OrderSide) -> Order:
        """
        Submit a market order.

        Parameters:
            symbol (str): The stock symbol to trade.
            qty (int): The quantity to trade.
            side (OrderSide): The side of the order (buy or sell).

        Returns:
            Order: The submitted order.
        """
        order = self.trading_client.submit_order(
            MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=side,
                time_in_force=TimeInForce.DAY
            )
        )
        return order

    def get_current_ask_price(self, symbol: str) -> float:
        """
        Get the current ask price for a given symbol.

        Parameters:
            symbol (str): The stock symbol to fetch the ask price for.

        Returns:
            float: The current ask price.
        """
        try:
            request = StockLatestQuoteRequest(symbol_or_symbols=[symbol])
            quotes_data = self.data_client.get_stock_latest_quote(request)
            if symbol in quotes_data:
                quote = quotes_data[symbol]
                return quote.ask_price
            else:
                print(f"No quote data available for {symbol}")
                return None
        except Exception as e:
            print(f"Exception in get_current_ask_price method for {symbol}: {str(e)}")
            return None

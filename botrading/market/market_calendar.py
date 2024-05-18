from datetime import datetime
import pandas as pd
import pandas_market_calendars as mcal
from ..enums import Exchange


class MarketCalendar:
    """
    MarketCalendar provides various functionalities to interact with market calendars.

    Attributes:
        exchange (Exchange): The exchange for which the calendar is created.
    """

    def __init__(self, exchange: Exchange):
        """
        Initializes the MarketCalendar with a specific exchange.

        Parameters:
            exchange (Exchange): The exchange for which the calendar is created.
        """
        self.exchange = exchange
        self.calendar = mcal.get_calendar(exchange.value)

    def get_timezone(self) -> str:
        """
        Gets the time zone of the exchange calendar.

        Returns:
            str: The time zone of the exchange calendar.
        """
        return self.calendar.tz.zone

    def get_last_holidays(self, num_holidays: int = 5) -> pd.DatetimeIndex:
        """
        Gets the last n holidays of the exchange calendar.

        Parameters:
            num_holidays (int): The number of holidays to retrieve.

        Returns:
            pd.DatetimeIndex: The list of last holidays as pandas Timestamps.
        """
        holidays = self.calendar.holidays()
        last_holidays = holidays.holidays[-num_holidays:]
        return pd.to_datetime(last_holidays)

    def get_market_times(self) -> dict:
        """
        Gets the regular market times of the exchange calendar.

        Returns:
            dict: A dictionary containing market times.
        """
        return self.calendar.regular_market_times

    def get_open_business_days(self, start_date: str, end_date: str) -> pd.DatetimeIndex:
        """
        Gets the open valid business days for the exchange between the given dates.

        Parameters:
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            pd.DatetimeIndex: The list of open business days.
        """
        return self.calendar.valid_days(start_date=start_date, end_date=end_date)

    def get_market_schedule(self, start_date: str, end_date: str, start: str = "regular", end: str = "regular") -> pd.DataFrame:
        """
        Gets the market schedule for the exchange between the given dates.

        Parameters:
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.
            start (str): The start time (e.g., "pre", "regular", "post").
            end (str): The end time (e.g., "pre", "regular", "post").

        Returns:
            pd.DataFrame: The market schedule.
        """
        return self.calendar.schedule(start_date=start_date, end_date=end_date, start=start, end=end)

    def get_early_closes(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Gets the early closes for the exchange between the given dates.

        Parameters:
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: The early close schedule.
        """
        schedule = self.calendar.schedule(start_date=start_date, end_date=end_date)
        return self.calendar.early_closes(schedule=schedule)

    def is_market_open_now(self) -> bool:
        """
        Checks if the market is open right now.

        Returns:
            bool: True if the market is open, False otherwise.
        """
        now_timestamp = pd.Timestamp(datetime.now(), tz=self.get_timezone())
        schedule = self.calendar.schedule(start_date=now_timestamp.strftime('%Y-%m-%d'), end_date=now_timestamp.strftime('%Y-%m-%d'))
        return self.calendar.open_at_time(schedule, now_timestamp)

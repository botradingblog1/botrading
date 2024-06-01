from datetime import datetime, timedelta
from ..enums import TimeInterval


def create_date_range(time_interval: TimeInterval, num_past_periods: int, date_format: str, end_date: datetime = None) -> tuple:
    """
    Creates start and end dates based on the specified time interval, number of past periods, and date format.

    Parameters:
        time_interval (TimeInterval): The time interval (DAYS, HOURS, SECONDS).
        num_past_periods (int): The number of past periods to calculate the start date.
        date_format (str): The date format to return the dates in.
        end_date (datetime): The end date. If None, defaults to the current date and time.

    Returns:
        tuple: A tuple containing the start date and end date in the specified format.

    Raises:
        ValueError: If the time interval is not recognized.
    """
    if end_date is None:
        end_date = datetime.today()

    if time_interval == TimeInterval.DAY:
        start_date = end_date - timedelta(days=num_past_periods)
    elif time_interval == TimeInterval.HOUR:
        start_date = end_date - timedelta(hours=num_past_periods)
    elif time_interval == TimeInterval.SECOND:
        start_date = end_date - timedelta(seconds=num_past_periods)
    elif time_interval == TimeInterval.MILLIS:
        start_date = end_date - timedelta(milliseconds=num_past_periods)
    else:
        raise ValueError("Invalid time interval specified. Must be one of: DAYS, HOURS, SECONDS.")

    return start_date.strftime(date_format), end_date.strftime(date_format)


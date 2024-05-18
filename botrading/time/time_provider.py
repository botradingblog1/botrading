import ntplib
from datetime import datetime
import pytz
import threading
import time
from ..enums import TimeZone


class TimeProvider:
    """
    TimeProvider is a singleton class that provides synchronized time using the NTP protocol.

    Attributes:
        time_offset (float): The offset between the system time and NTP time.
        last_sync (datetime): The last time the synchronization was performed.
        timezone (pytz.timezone): The timezone to be used for time conversion.
        sync_interval (int): The interval in seconds between each synchronization.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, timezone: TimeZone = TimeZone.US_EASTERN, sync_interval: int = 60 * 60):
        """
        Ensures that only one instance of TimeProvider is created (Singleton pattern).

        Parameters:
            timezone (TimeZone): The timezone for the TimeProvider.
            sync_interval (int): The interval in seconds between each synchronization.

        Returns:
            TimeProvider: The singleton instance of TimeProvider.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(TimeProvider, cls).__new__(cls)
                cls._instance.time_offset = None
                cls._instance.last_sync = None
                cls._instance.timezone = pytz.timezone(timezone.value)
                cls._instance.sync_interval = sync_interval
                cls._instance.sync_time()
                cls._instance.start_auto_sync()
        return cls._instance

    def sync_time(self):
        """
        Synchronizes the system time with the NTP server time.
        """
        client = ntplib.NTPClient()
        try:
            response = client.request('pool.ntp.org')
            self.time_offset = response.tx_time - time.time()
            self.last_sync = datetime.now(pytz.utc)
            print(f"Time synchronized successfully. Last sync: {self.last_sync}")
        except Exception as e:
            print(f"Failed to sync time: {e}")
            self.time_offset = None  # Use system time if sync fails

    def get_datetime(self) -> datetime:
        """
        Gets the current date and time considering the NTP time offset.

        Returns:
            datetime: The current date and time in the set timezone.
        """
        current_time = datetime.now(pytz.utc) if self.time_offset is None else datetime.fromtimestamp(
            time.time() + self.time_offset, pytz.utc)
        return current_time.astimezone(self.timezone)

    def get_date(self) -> datetime.date:
        """
        Gets the current date.

        Returns:
            datetime.date: The current date in the set timezone.
        """
        return self.get_datetime().date()

    def get_time(self) -> datetime.time:
        """
        Gets the current time.

        Returns:
            datetime.time: The current time in the set timezone.
        """
        return self.get_datetime().time()

    def set_timezone(self, timezone: TimeZone):
        """
        Sets the timezone for the TimeProvider.

        Parameters:
            timezone (TimeZone): The timezone enum value.
        """
        self.timezone = pytz.timezone(timezone.value)
        print(f"Timezone set to: {self.timezone}")

    def start_auto_sync(self):
        """
        Starts automatic time synchronization at the specified interval.
        """

        def sync():
            while True:
                self.sync_time()
                time.sleep(self.sync_interval)

        print(f"Starting auto-sync every {self.sync_interval} seconds.")
        threading.Thread(target=sync, daemon=True).start()

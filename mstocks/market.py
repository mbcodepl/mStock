from datetime import datetime, time as datetime_time
import pytz

class Market:
    EASTERN = pytz.timezone('US/Eastern')
    CENTRAL_EUROPEAN = pytz.timezone('Europe/Warsaw')

    US_MARKET_OPEN = datetime_time(9, 30, 0)
    US_MARKET_CLOSE = datetime_time(16, 0, 0)
    WARSAW_MARKET_OPEN = datetime_time(9, 0, 0)
    WARSAW_MARKET_CLOSE = datetime_time(17, 0, 0)

    def __init__(self, utils):
        self.utils = utils

    def is_market_open(self, symbol):
        now = None
        market_open = None
        market_close = None
        if ".WA" in symbol:  # Warsaw market
            now = datetime.now(Market.CENTRAL_EUROPEAN)
            market_open = Market.WARSAW_MARKET_OPEN
            market_close = Market.WARSAW_MARKET_CLOSE
        else:  # Default to US market
            now = datetime.now(Market.EASTERN)
            market_open = Market.US_MARKET_OPEN
            market_close = Market.US_MARKET_CLOSE

        is_open = market_open <= now.time() <= market_close and now.weekday() < 5
        return (f"{self.utils.GREEN}●{self.utils.RESET}" if is_open else f"{self.utils.RED}●{self.utils.RESET}"), now.strftime('%H:%M:%S')

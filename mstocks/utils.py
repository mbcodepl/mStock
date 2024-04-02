import re
class Utils:
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def get_currency(symbol, currency_map):
        for key in currency_map:
            if symbol.endswith(key):
                return currency_map[key]
        return "USD"  # Default to USD if not found
    
    @staticmethod
    def strip_ansi_codes(text):
        """
        Removes ANSI color/style sequences from a string.
        """
        ansi_escape = re.compile(r'(?:\x1b\[|\x9b)[0-?]*[ -\/]*[@-~]')
        return ansi_escape.sub('', text)

    @staticmethod
    def print_table_with_fixed_width(prices, include_market_status=True):
        # Define colors for positive and negative earnings
        POSITIVE_EARNINGS = Utils.OKGREEN
        NEGATIVE_EARNINGS = Utils.FAIL
        # Adjust headers based on whether to include market status
        headers = ['-', 'Hour', 'Symbol', 'Name', 'Price', 'Trend', 'Invested', 'Earnings'] if include_market_status else ['Hour', 'Symbol', 'Name', 'Price', 'Trend', 'Invested', 'Earnings']
        
        # Strip extra spaces from the headers
        headers = [header.strip() for header in headers]

        max_widths = [0] * len(headers)
        for row in prices:
            for i, item in enumerate(row):
                length = len(Utils.strip_ansi_codes(str(item)))
                if length > max_widths[i]:
                    max_widths[i] = length

        # Include headers in the max_widths calculation
        for i, header in enumerate(headers):
            length = len(header)
            if length > max_widths[i]:
                max_widths[i] = length

        # Create a horizontal separator
        horizontal_sep = '-' * (sum(max_widths) + (3 * (len(max_widths) - 1)))

        # Print headers with bold style
        format_str = ' | '.join(f"{Utils.BOLD}{{:<{w}}}{Utils.ENDC}" for w in max_widths)
        print(format_str.format(*headers))
        print(horizontal_sep)

        # Print each row
        for row in prices:
            formatted_row = []
            for i, item in enumerate(row):
                item_str = str(item)

                # Apply color coding to Trend column (assuming it's the second to last column)
                if '↑' in item_str:
                    item_str = Utils.OKGREEN + item_str + Utils.ENDC
                elif '↓' in item_str:
                    item_str = Utils.FAIL + item_str + Utils.ENDC
                
                # Apply color coding to Earnings column (assuming it's the last column)
                if i == len(row) - 1:
                    if item_str != '—':  # Check if earnings is not the placeholder
                        # Apply strip_ansi_codes here
                        item_str_clean = Utils.strip_ansi_codes(item_str)
                        earnings_value = float(item_str_clean.split()[0])
                        if earnings_value > 0:
                            item_str = POSITIVE_EARNINGS + item_str + Utils.ENDC
                        elif earnings_value < 0:
                            item_str = NEGATIVE_EARNINGS + item_str + Utils.ENDC

                formatted_row.append(item_str)

            # Print the row with the dynamic format string
            print(format_str.format(*formatted_row))

    @staticmethod
    def _format_value(value, currency, percent_change=None):
        """
        Formats a value with currency and optional percent change, including color coding and directional arrows.
        Designed to replace and combine the functionalities of _format_trend and _format_earnings.

        :param value: The numeric value to be formatted, such as earnings or price change.
        :param currency: The currency symbol as a string.
        :param percent_change: Optional. The percent change as a float. When provided, it's included in the formatted output.
        :return: A string formatted with value, currency, optional percent change, and directional arrows, all color-coded.
        """
        # Color and direction are determined by the value.
        color = Utils.GREEN if value > 0 else Utils.RED if value < 0 else ""
        direction = "↑" if value > 0 else "↓" if value < 0 else ""
        
        # Format the basic string with value and currency.
        formatted_str = f"{color}{value:+.2f} {currency}"
        
        # If there's a percent change, append it.
        if percent_change is not None:
            formatted_str += f" ({abs(percent_change):.2f}%)"
        
        # Add the direction symbol if the value is not zero.
        if value != 0:
            formatted_str += f" {direction}"
        
        # Reset the color at the end.
        formatted_str += f"{Utils.RESET}" if color else ""
        
        return formatted_str    


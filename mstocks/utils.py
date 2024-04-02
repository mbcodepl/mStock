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
        if include_market_status:
            headers = ['Market status', 'Hour', 'Symbol', 'Name', 'Price', 'Trend', 'Invested', 'Earned %', 'Earnings']
        else:
            headers = ['Hour', 'Symbol', 'Name', 'Price', 'Trend', 'Invested', 'Earned %', 'Earnings']
        
        max_widths = [0] * len(headers)
        for row in prices:
            for i, item in enumerate(row):
                # Use unicode_escape to better handle different character lengths
                length = len(str(item).encode('unicode_escape').decode())
                if length > max_widths[i]:
                    max_widths[i] = length
        
        # Create a horizontal separator
        horizontal_sep = '-' * (sum(max_widths) + (3 * len(max_widths)))

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
                        earnings_value = float(item_str.split()[0])
                        if earnings_value > 0:
                            item_str = POSITIVE_EARNINGS + item_str + Utils.ENDC
                        elif earnings_value < 0:
                            item_str = NEGATIVE_EARNINGS + item_str + Utils.ENDC

                formatted_row.append(item_str)

            # Print the row with the dynamic format string
            print(format_str.format(*formatted_row))
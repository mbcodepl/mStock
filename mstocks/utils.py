class Utils:
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    @staticmethod
    def get_currency(symbol, currency_map):
        for key in currency_map:
            if symbol.endswith(key):
                return currency_map[key]
        return "USD"  # Default to USD if not found

    @staticmethod
    def print_table_with_fixed_width(prices):
        max_widths = [0] * len(prices[0])
        for row in prices:
            for i, item in enumerate(row):
                length = len(str(item).encode().decode('unicode_escape').encode('ascii', 'ignore').decode())
                if length > max_widths[i]:
                    max_widths[i] = length
        format_str = ' | '.join(f"{{:<{w}}}" for w in max_widths)
        headers = ['Market status', 'Hour', 'Symbol', 'Name', 'Price', 'Trend']
        print(format_str.format(*headers))
        print('-' * sum(max_widths) + '-----' * (len(max_widths) - 1))
        for row in prices:
            print(format_str.format(*row))

from colorama import Fore

from config.config import settings

def logger(self, message, log_type="info"):
    address = self.item_data['address']
    masked_address = f"{address[:6]}...{address[-6:]}"

    colors = [
        "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m",
        "\033[96m", "\033[90m", "\033[97m", "\033[35m", "\033[36m"
    ]
    reset = "\033[0m"
    color = colors[self.account_index % len(colors)]

    account_index_str = f"{self.account_index + 1}".rjust(2)
    address_str = masked_address.ljust(13) 
    ip_str = "Local IP".ljust(15)
    if settings['USE_PROXY']:
        ip_str = (self.proxy_ip if self.proxy_ip else "Unknown IP").ljust(15)

    prefix = Fore.LIGHTBLACK_EX + f"[{address_str}][{ip_str}]{reset}"
    log_message = f"{prefix}{color}[{account_index_str}]{reset} {message}"
    print(log_message)
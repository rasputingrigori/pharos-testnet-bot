# Pharos Testnet Automation Scripts

### Description
Pharos testnet (Incentives) bot - an automations python script to interact with the platfom like Check-in, Claim Faucet, Swap (All Pair), Add Liquidity (All Pair), send token, complete quest and Auto Referral.

### Features
-  Multithread support: Run your bot faster (10 account with default setting completely in 5 minutes)

-  **Claim Faucet**: Support auto claiming official faucet

-  **Captcha Solver**: Completing captcha for faucet

-  **Check-in**: Support Daily Checkin without missing a day

-  **Proxy Support**: Supports both mobile and regular proxies.

-  **Auto Referral**: Support to Register a new account with Referral

-  **Wallet Handling**: Shuffle wallets and `configure` pauses between operations.

-  **Token Swaps**: Supports ALL PAIR eg: `USDT-USDC, PHRS-USDT, PHRS-USDC, WPHRS-USDT, WPHRS-USDC` 

-  **Liquidity**: Support Deposit ALL PAIR eg: `USDT-USDC, WPHRS-USDT, WPHRS-USDC` 

-  **WRAP/UNWRAP**: Support Wrapping `PHRS to WPHRS` and Unwrapping `WPHRS to PHRS`

-  **Quest Completion**: Support automatic quest completions (must connect x)

* **Randomized User Agents:** Generates random, yet plausible, user agents for each account.

## Prerequisites

* Python 3.8 or higher
* `pip` (Python package installer)

### Installation and startup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rasputingrigori/pharos-testnet-bot.git
   cd pharos-testnet-bot
   ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
     ```
    ### On Windows
    ```bash
    venv\Scripts\activate
    ```
    ### On macOS/Linux
    ```bash
    source venv/bin/activate
    ```

4.  **Install dependencies:**

    The `requirements.txt` ensure your `requirements.txt` looks like this before installing:
    ```txt
    aiohttp>=3.9.0
    asyncio
    requests>=2.31.0
    web3>=6.0.0
    eth-account>=0.10.0
    pyjwt>=2.8.0
    python-dotenv>=1.0.1
    colorama>=0.4.6
    aiofiles==23.2.1
    ```
    Then install:
    ```bash
    pip install -r requirements.txt
    ```

5.  **`private_key.txt`:**
    * Create a file named `private_key.txt` in the root directory of the project (same level as `main.py`).
    * Add your Ethereum private keys to this file, one private key per line.
    * Keys can be with or without the `0x` prefix.
    * Example:
        ```yaml
        0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
        fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321
        ```

6. Add your Proxies on `proxies.txt`
    ```yaml
    http://login:pass@ip:port
    http://login:pass@ip:port
    ```

7. Add referral & wallet
   - Change or Create `example.env` to `.env` and fill your referral code on `REF_CODE`
   - Fill the `wallet.txt` with your receiver token address
    
8. Run (first module, then second module):
   ```bash
    python main.py
   ```

## Configuration
All settings are in `.env`. Key options include:

### Feature Settings
    ```yaml
    AUTO_FAUCET=false

    AUTO_LIQUIDITY=true
    NUMBER_LIQUIDITY=1
    AMOUNT_LIQUIDITY = [1, 5]  # This means 1%-5% of token0 will be used

    AUTO_SEND=true
    NUMBER_SEND=1
    AMOUNT_SEND=[0.01,0.022]

    AUTO_WRAP=false
    AUTO_UNWRAP=false
    NUMBER_WRAP_UNWRAP=1
    AMOUNT_WRAP_UNWRAP=[0.1,0.21]

    AUTO_SWAP=false
    NUMBER_SWAP=1
    AMOUNT_SWAP=[1,2]

    AUTO_CHECKIN=false
    ```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, features, or improvements.

## Disclaimer

* This bot is intended for educational and testing purposes, particularly for interacting with the Pharos testnet environment.
* Users are solely responsible for ensuring their use of this bot complies with Pharos's terms of service and any applicable platform policies.
* The maintainers of this project are not responsible for any misuse, account restrictions, or other consequences arising from the use of this bot.

## License

This project is open-source—modify with "[MIT License](?tab=MIT-1-ov-file)" and distribute as needed.

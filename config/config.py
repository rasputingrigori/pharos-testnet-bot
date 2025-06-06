import os
import json
from dotenv import load_dotenv
from src.utils.utils import _is_array

load_dotenv()

settings = {
    "TIME_SLEEP": int(os.getenv("TIME_SLEEP", 8)),
    "MAX_THREADS": int(os.getenv("MAX_THREADS", 10)),
    "MAX_LEVEL_SPEED": int(os.getenv("MAX_LEVEL_SPEED", 10)),
    "MAX_THREADS_NO_PROXY": int(os.getenv("MAX_THREADS_NO_PROXY", 10)),
    "NUMBER_SEND": int(os.getenv("NUMBER_SEND", 10)),
    "NUMBER_SWAP": int(os.getenv("NUMBER_SWAP", 10)),
    "NUMBER_STAKE": int(os.getenv("NUMBER_STAKE", 10)),
    "NUMBER_WRAP_UNWRAP": int(os.getenv("NUMBER_WRAP_UNWRAP", 10)),

    "SKIP_TASKS": json.loads(os.getenv("SKIP_TASKS", "[]").replace("'", '"')),
    "TASKS_ID": json.loads(os.getenv("TASKS_ID", "[]").replace("'", '"')),
    "AUTO_TASK": os.getenv("AUTO_TASK", "false").lower() == "true",
    "ENABLE_DEBUG": os.getenv("ENABLE_DEBUG", "false").lower() == "true",
    "AUTO_STAKE": os.getenv("AUTO_STAKE", "false").lower() == "true",
    "AUTO_CHECKIN": os.getenv("AUTO_CHECKIN", "false").lower() == "true",

    "USE_PROXY": os.getenv("USE_PROXY", "false").lower() == "true",
    "AUTO_FAUCET": os.getenv("AUTO_FAUCET", "false").lower() == "true",
    "AUTO_SWAP": os.getenv("AUTO_SWAP", "false").lower() == "true",
    "AUTO_SEND": os.getenv("AUTO_SEND", "false").lower() == "true",
    "AUTO_WRAP": os.getenv("AUTO_WRAP", "false").lower() == "true",
    "AUTO_UNWRAP": os.getenv("AUTO_UNWRAP", "false").lower() == "true",

    "API_ID": os.getenv("API_ID", None),
    "BASE_URL": os.getenv("BASE_URL", None),
    "REF_CODE": os.getenv("REF_CODE", "6KrCMbaT8IZqPYUm"),
    "RPC_URL": os.getenv("RPC_URL", "https://api.zan.top/node/v1/pharos/testnet/1761472bf26745488907477d23719fb5"),
    "CHAIN_ID": os.getenv("CHAIN_ID", 688688),

    "TYPE_CAPTCHA": os.getenv("TYPE_CAPTCHA", None),
    "API_KEY_2CAPTCHA": os.getenv("API_KEY_2CAPTCHA", None),
    "API_KEY_ANTI_CAPTCHA": os.getenv("API_KEY_ANTI_CAPTCHA", None),
    "CAPTCHA_URL": os.getenv("CAPTCHA_URL", None),
    "WEBSITE_KEY": os.getenv("WEBSITE_KEY", None),

    'DELAY_BETWEEN_REQUESTS': json.loads(os.getenv('DELAY_BETWEEN_REQUESTS')) if _is_array(os.getenv('DELAY_BETWEEN_REQUESTS')) else [1, 5],
    'DELAY_START_BOT': json.loads(os.getenv('DELAY_START_BOT')) if _is_array(os.getenv('DELAY_START_BOT')) else [1, 15],
    'PERCENT_STAKE': json.loads(os.getenv('PERCENT_STAKE')) if _is_array(os.getenv('PERCENT_STAKE')) else [1, 15],
    'DELAY_TASK': json.loads(os.getenv('DELAY_TASK')) if _is_array(os.getenv('DELAY_TASK')) else [10, 15],
    'AMOUNT_SEND': json.loads(os.getenv('AMOUNT_SEND')) if _is_array(os.getenv('AMOUNT_SEND')) else [0.1, 0.2],
    'AMOUNT_SWAP': json.loads(os.getenv('AMOUNT_SWAP')) if _is_array(os.getenv('AMOUNT_SWAP')) else [0.03, 0.05],           # default: 3%–5%
    'AMOUNT_WRAP_UNWRAP': json.loads(os.getenv('AMOUNT_WRAP_UNWRAP')) if _is_array(os.getenv('AMOUNT_WRAP_UNWRAP')) else [0.02, 0.04],  # default: 2%–4%

    "AUTO_LIQUIDITY": os.getenv("AUTO_LIQUIDITY", "false").lower() == "true",
    "NUMBER_LIQUIDITY": int(os.getenv("NUMBER_LIQUIDITY", 1)),
    "AMOUNT_LIQUIDITY": json.loads(os.getenv("AMOUNT_LIQUIDITY")) if _is_array(os.getenv("AMOUNT_LIQUIDITY")) else [3, 7],

}

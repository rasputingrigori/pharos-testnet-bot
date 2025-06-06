import os
import re
import json
import time
import random
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import jwt as pyjwt

from src.helpers.file import TOKENS_FILE, ENV_FILE_PATH

load_dotenv()
lock = asyncio.Lock()

def update_env(variable, value):
    try:
        with open(ENV_FILE_PATH, 'r', encoding='utf-8') as file:
            content = file.read()

        pattern = f'^{variable}=.*'
        updated = re.sub(pattern, f'{variable}={value}', content, flags=re.MULTILINE)

        if not re.search(pattern, content):
            updated += f'\n{variable}={value}'

        with open(ENV_FILE_PATH, 'w', encoding='utf-8') as file:
            file.write(updated)
    except Exception as e:
        print(f"Cannot read/write .env file: {e}", "error")

def sleep(seconds=None):
    if isinstance(seconds, (int, float)):
        time.sleep(seconds)
        return

    delay = random.randint(*(seconds if isinstance(seconds, list) else [1, 5]))
    time.sleep(delay)

def random_delay():
    delay_range = os.getenv("DELAY_REQUEST_API", "[1,5]")
    try:
        min_delay, max_delay = json.loads(delay_range)
        time.sleep(random.randint(min_delay, max_delay))
    except Exception:
        print("Invalid DELAY_REQUEST_API format. Expected JSON list like [1, 5]", "warning")

def save_token(user_id, token):
    tokens = {}
    if os.path.exists("tokens.json"):
        with open("tokens.json", "r", encoding='utf-8') as file:
            tokens = json.load(file)
    tokens[user_id] = token
    with open("tokens.json", "w", encoding='utf-8') as file:
        json.dump(tokens, file, indent=4)

def get_token(user_id):
    if os.path.exists("tokens.json"):
        with open("tokens.json", "r", encoding='utf-8') as file:
            return json.load(file).get(user_id)
    return None

def is_token_expired(token):
    def current_time_str():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not token or token.count('.') != 2:
        return {'isExpired': True, 'expirationDate': current_time_str()}

    try:
        payload = pyjwt.decode(token, options={"verify_signature": False})
        exp = payload.get('exp')
        if not isinstance(exp, (int, float)):
            return {'isExpired': True, 'expirationDate': current_time_str()}

        now = time.time()
        is_expired = now > exp
        expiration = datetime.fromtimestamp(exp).strftime("%Y-%m-%d %H:%M:%S")
        return {
            'isExpired': is_expired,
            'expirationDate': expiration
        }

    except Exception as e:
        print(f"Token check error: {e}", "error")
        return {'isExpired': True, 'expirationDate': current_time_str()}

async def save_json(identifier, value, filename=TOKENS_FILE):
    async with lock:
        data = {}
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        data[identifier] = value

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

def load_token_data(identifier, filename=TOKENS_FILE):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            all_tokens = json.load(f)
        data = all_tokens.get(identifier)
        return data
    return None

def load_data(file_path):
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            lines = [line for line in f.read().replace('\r', '').split('\n') if line]
        if not lines:
            print(f"No data found in {file_path}", "warning")
        return lines
    except Exception as e:
        print(f"Error loading file {file_path}: {e}", "error")
        return []

def get_item(identifier, filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file).get(identifier)
    return None

def _is_array(obj):
    try:
        return isinstance(obj, list) and len(obj) > 0 or isinstance(json.loads(obj), list)
    except Exception:
        return False
    
def load_abi(filename):
    with open(f"abi/{filename}", "r", encoding="utf-8") as file:
        return json.load(file)


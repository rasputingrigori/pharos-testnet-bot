import time
from web3 import Web3
from eth_account import Account
from decimal import Decimal, getcontext
from threading import Lock

from config.config import settings
from .helpers.generators import s0x999
from .helpers.address import (
    WPHRS_ADDRESS, 
    USDC_ADDRESS, USDT_ADDRESS, 
    SWAP_ROUTER_ADDRESS, POSITION_MANAGER_ADDRESS, 
    )
from .helpers.abi import ( 
    SWAP_ABI, ERC20_ABI, ROUTER_ABI, 
    UNISWAP_POOL_ABI, POSITION_MANAGER_ABI
    )

wallet_locks = {}
getcontext().prec = 28

web3 = Web3(Web3.HTTPProvider(settings['RPC_URL']))
EXPLORER_URL = "https://testnet.pharosscan.xyz/tx/"
CHAIN_ID = 688688

def get_wallet_lock(address):
    if address not in wallet_locks:
        wallet_locks[address] = Lock()
    return wallet_locks[address]

def swap_token(params):
    web3 = Web3(Web3.HTTPProvider(params['provider']))
    account = Account.from_key(params['private_key'])
    wallet = account.address

    token_map = {
        "WPHRS": WPHRS_ADDRESS,
        "USDT": USDT_ADDRESS,
        "USDC": USDC_ADDRESS,
        "PHRS": WPHRS_ADDRESS
    }

    token_in_symbol = params['token_in']
    token_out_symbol = params['token_out']
    if isinstance(params['amount'], float) and 0 < params['amount'] < 100:

        token_address = token_map[params['token_in']]
        if token_address:
            token_contract = web3.eth.contract(address=token_address, abi=ERC20_ABI)
            balance_raw = token_contract.functions.balanceOf(wallet).call()
            decimals = token_contract.functions.decimals().call()
            human_balance = Decimal(balance_raw) / Decimal(10**decimals)
        else:
            balance_raw = web3.eth.get_balance(wallet)
            human_balance = Decimal(balance_raw) / Decimal(10**18)

        amount_value = (Decimal(params['amount']) / Decimal(100)) * human_balance
        amount = web3.to_wei(amount_value, 'ether')
    else:
        amount = web3.to_wei(params['amount'], 'ether')

    token_in = token_map[token_in_symbol]
    token_out = token_map[token_out_symbol]
    router = web3.eth.contract(address=SWAP_ROUTER_ADDRESS, abi=ROUTER_ABI)
    token_contract = web3.eth.contract(address=token_in, abi=ERC20_ABI)
    allowance = token_contract.functions.allowance(wallet, SWAP_ROUTER_ADDRESS).call()

    if allowance < amount:
        approve_tx = token_contract.functions.approve(SWAP_ROUTER_ADDRESS, amount).build_transaction({
            "from": wallet,
            "nonce": web3.eth.get_transaction_count(wallet),
            "gas": 50000,
            "gasPrice": web3.to_wei("1", "gwei")
        })
        signed_approve = web3.eth.account.sign_transaction(approve_tx, params['private_key'])
        approve_hash = web3.eth.send_raw_transaction(signed_approve.raw_transaction)
        web3.eth.wait_for_transaction_receipt(approve_hash)

    exact_input = router.functions.exactInputSingle({
        "tokenIn": token_in,
        "tokenOut": token_out,
        "fee": 3000,
        "recipient": wallet,
        "amountIn": amount,
        "amountOutMinimum": 0,
        "sqrtPriceLimitX96": 0
    }).build_transaction({
        "from": wallet,
        "nonce": web3.eth.get_transaction_count(wallet),
        "gas": 300000,
        "gasPrice": web3.to_wei("1", "gwei")
    })

    encoded = exact_input["data"]
    deadline = int(time.time()) + 600

    multicall_tx = router.functions.multicall(deadline, [encoded]).build_transaction({
        "from": wallet,
        "nonce": web3.eth.get_transaction_count(wallet),
        "gas": 400000,
        "gasPrice": web3.to_wei("1", "gwei")
    })

    signed = web3.eth.account.sign_transaction(multicall_tx, params['private_key'])
    tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    tx_url = f"{EXPLORER_URL}{web3.to_hex(tx_hash)}"
    short_url = s0x999(tx_url)
    return {
        "tx": web3.to_hex(tx_hash),
        "success": receipt.status == 1,
        "message": f"Swap {token_in_symbol} → {token_out_symbol} {'success' if receipt.status == 1 else 'failed'}: Transaction Hash: {short_url}"
    }

def wrap_token(params):
    action = params['action']
    amount = params['amount']
    private_key = params['private_key']
    rpc_url = params['provider']

    web3 = Web3(Web3.HTTPProvider(rpc_url))
    account = Account.from_key(private_key)
    wallet_address = account.address
    contract = web3.eth.contract(address=WPHRS_ADDRESS, abi=SWAP_ABI)

    try:
        phrs_balance = web3.eth.get_balance(wallet_address)
        if phrs_balance < web3.to_wei("0.0001", "ether"):
            return {
                "tx": None,
                "success": False,
                "message": "Insufficient PHRS for transaction fees",
            }

        amount_wei = web3.to_wei(str(amount), "ether")
        nonce = web3.eth.get_transaction_count(wallet_address, 'pending') 
        gas_price = web3.to_wei("1", "gwei")

        if action == "unwrap":
            wphrs_contract = web3.eth.contract(address=WPHRS_ADDRESS, abi=ERC20_ABI)
            wphrs_balance = wphrs_contract.functions.balanceOf(wallet_address).call()

            if wphrs_balance < amount_wei:
                action = "wrap"

        if action == "wrap":
            tx = contract.functions.deposit().build_transaction({
                "from": wallet_address,
                "value": amount_wei,
                "gas": 60000,
                "gasPrice": gas_price,
                "nonce": nonce,
                "chainId": CHAIN_ID
            })
        elif action == "unwrap":
            tx = contract.functions.withdraw(amount_wei).build_transaction({
                "from": wallet_address,
                "gas": 60000,
                "gasPrice": gas_price,
                "nonce": nonce,
                "chainId": CHAIN_ID
            })
        else:
            return {
                "tx": None,
                "success": False,
                "message": f"Invalid action: {action}"
            }

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_url = f"{EXPLORER_URL}{web3.to_hex(tx_hash)}"
        short_url = s0x999(tx_url)

        return {
            "tx": web3.to_hex(tx_hash),
            "success": receipt.status == 1,
            "message": f"{action.title()} {amount} {'success' if receipt.status == 1 else 'failed'}: Transaction Hash: {short_url}",
        }

    except Exception as error:
        return {
            "tx": None,
            "success": False,
            "message": f"{action.title()} {amount} failed: {str(error)}",
        }

def check_balance(params):
    token_address = params.get('address')
    provider_url = params.get('provider')
    private_key = params.get('privateKey')
    abi = params.get('abi', ERC20_ABI) 

    if not provider_url or not private_key:
        print("Missing provider or privateKey in parameters.", "error")
        return "0"

    web3 = Web3(Web3.HTTPProvider(provider_url))
    account = web3.eth.account.from_key(private_key)
    wallet_address = account.address

    try:
        if token_address:
            token_contract = web3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=abi
            )
            balance = token_contract.functions.balanceOf(wallet_address).call()
            decimals = token_contract.functions.decimals().call()
            human_balance = Decimal(balance) / Decimal(10**decimals)
        else:
            balance = web3.eth.get_balance(wallet_address)
            human_balance = Decimal(balance) / Decimal(10**18)

        return format(human_balance, '.4f')

    except Exception as error:
        print(f"[{wallet_address}] Failed to check balance: {str(error)}", "error")
        return "0"

def send_token(params):
    recipient_address = params['recipient_address']
    amount = params['amount']
    private_key = params['private_key']
    provider_url = params['provider']

    web3 = Web3(Web3.HTTPProvider(provider_url))
    account = Account.from_key(private_key)
    wallet_address = account.address

    try:
        amount_in_wei = web3.to_wei(str(amount), 'ether')
        balance = web3.eth.get_balance(wallet_address)

        if balance < web3.to_wei("0.0001", "ether"):
            return {
                "tx": None,
                "success": False,
                "message": "Insufficient PHRS for transfer",
            }

        min_required = amount_in_wei + web3.to_wei("0.000021", "ether")
        if balance < min_required:
            return {
                "tx": None,
                "success": False,
                "message": f"Insufficient PHRS. Need at least {web3.from_wei(min_required, 'ether')} PHRS, have {web3.from_wei(balance, 'ether')} PHRS.",
            }

        gas_price = web3.to_wei("1", "gwei")
        nonce = web3.eth.get_transaction_count(wallet_address, 'pending')

        tx = {
            "to": Web3.to_checksum_address(recipient_address),
            "value": amount_in_wei,
            "gas": 21000,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": CHAIN_ID
        }

        signed_tx = Account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_hex = web3.to_hex(tx_hash)
        web3.eth.wait_for_transaction_receipt(tx_hash)

        tx_url = f"{EXPLORER_URL}{web3.to_hex(tx_hash)}"
        short_url = s0x999(tx_url)
        return {
            "tx": tx_hash_hex,
            "success": True,
            "message": f"Send {amount} PHRS! Transaction Hash: {short_url}",
        }

    except Exception as error:
        return {
            "tx": None,
            "success": False,
            "message": f"Error Send: {str(error)}",
        }

def approve_token(token, amount, wallet, web3, router, private_key):
    contract = web3.eth.contract(address=token, abi=ERC20_ABI)
    current_allowance = contract.functions.allowance(wallet, router.address).call()

    if current_allowance < amount:
        tx = contract.functions.approve(router.address, amount).build_transaction({
            "from": wallet,
            "nonce": web3.eth.get_transaction_count(wallet),
            "gas": 50000,
            "gasPrice": web3.to_wei("1", "gwei")
        })
        signed = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
        web3.eth.wait_for_transaction_receipt(tx_hash)

def add_liquidity_uniswap_v3(params):
    web3 = Web3(Web3.HTTPProvider(params["provider"]))
    account = Account.from_key(params["private_key"])
    wallet = account.address

    token_map = {
        "USDC": USDC_ADDRESS,
        "USDT": USDT_ADDRESS,
        "WPHRS": WPHRS_ADDRESS
    }

    token0_symbol = params["token0"]
    token1_symbol = params["token1"]
    token_in_symbol = params["input_token"]
    input_amount = Decimal(params["amount"])

    if token_map[token0_symbol].lower() > token_map[token1_symbol].lower():
        token0_symbol, token1_symbol = token1_symbol, token0_symbol
        token_in_symbol = token1_symbol if token_in_symbol == token0_symbol else token0_symbol

    token0 = Web3.to_checksum_address(token_map[token0_symbol])
    token1 = Web3.to_checksum_address(token_map[token1_symbol])

    pool_map = {
        ("WPHRS", "USDC"): "0xfe96fada81f089a4ca14550d89637a12bd8210e7",
        ("USDC", "USDT"): "0x208ab2365955d6809b6afccb3f7d0822e10ae69f",
        ("WPHRS", "USDT"): "0x65709ab438ac75e85993b9edb8c2e8060d8fd7c3"
    }

    pool_address = pool_map.get((token0_symbol, token1_symbol)) or pool_map.get((token1_symbol, token0_symbol))
    if not pool_address:
        raise Exception("Unknown pool address.")
    pool_address = Web3.to_checksum_address(pool_address)

    pool_contract = web3.eth.contract(address=pool_address, abi=UNISWAP_POOL_ABI)
    sqrt_price_x96 = pool_contract.functions.slot0().call()[0]
    price = (Decimal(sqrt_price_x96) / (1 << 96)) ** 2

    if token0_symbol == token_in_symbol:
        amount0 = input_amount
        amount1 = input_amount * price
    else:
        amount1 = input_amount
        amount0 = input_amount / price

    token0_contract = web3.eth.contract(address=token0, abi=ERC20_ABI)
    token1_contract = web3.eth.contract(address=token1, abi=ERC20_ABI)

    dec0 = token0_contract.functions.decimals().call()
    dec1 = token1_contract.functions.decimals().call()

    raw_amount0 = int(amount0 * (10 ** dec0))
    raw_amount1 = int(amount1 * (10 ** dec1))

    manager_contract = web3.eth.contract(address=Web3.to_checksum_address(POSITION_MANAGER_ADDRESS), abi=POSITION_MANAGER_ABI)

    nonce = web3.eth.get_transaction_count(wallet)

    for token_contract, raw_amount in [(token0_contract, raw_amount0), (token1_contract, raw_amount1)]:
        allowance = token_contract.functions.allowance(wallet, manager_contract.address).call()
        if allowance < raw_amount:
            tx = token_contract.functions.approve(manager_contract.address, raw_amount).build_transaction({
                "from": wallet,
                "nonce": nonce,
                "gas": 100_000,
                "gasPrice": web3.to_wei("1", "gwei"),
                "chainId": CHAIN_ID
            })
            signed_tx = web3.eth.account.sign_transaction(tx, params["private_key"])
            web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            web3.eth.wait_for_transaction_receipt(signed_tx.hash)
            nonce += 1

    deadline = int(time.time()) + 600
    fee = 3000
    tick_lower = -60000
    tick_upper = 60000

    existing_token_id = None
    balance = manager_contract.functions.balanceOf(wallet).call()
    for i in range(balance):
        token_id = manager_contract.functions.tokenOfOwnerByIndex(wallet, i).call()
        pos = manager_contract.functions.positions(token_id).call()
        if (
            pos[2].lower() == token0.lower() and
            pos[3].lower() == token1.lower() and
            pos[4] == fee and
            pos[5] == tick_lower and
            pos[6] == tick_upper
        ):
            existing_token_id = token_id
            break

    datas = []

    try:
        if existing_token_id:
            tx_data = manager_contract.functions.increaseLiquidity({
                "tokenId": existing_token_id,
                "amount0Desired": raw_amount0,
                "amount1Desired": raw_amount1,
                "amount0Min": 0,
                "amount1Min": 0,
                "deadline": deadline
            }).build_transaction({"from": wallet})["data"]
        else:
            tx_data = manager_contract.functions.mint({
                "token0": token0,
                "token1": token1,
                "fee": fee,
                "tickLower": tick_lower,
                "tickUpper": tick_upper,
                "amount0Desired": raw_amount0,
                "amount1Desired": raw_amount1,
                "amount0Min": 0,
                "amount1Min": 0,
                "recipient": wallet,
                "deadline": deadline
            }).build_transaction({"from": wallet})["data"]
        datas.append(tx_data)

        encoded_refund = manager_contract.functions.refundETH().build_transaction({"from": wallet})["data"]
        datas.append(encoded_refund)

        multicall_tx = manager_contract.functions.multicall(datas).build_transaction({
            "from": wallet,
            "nonce": nonce,
            "gas": 1_500_000,
            "gasPrice": web3.to_wei("1", "gwei"),
            "value": 0,
            "chainId": CHAIN_ID
        })

        signed_tx = web3.eth.account.sign_transaction(multicall_tx, params["private_key"])
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        tx_url = f"{EXPLORER_URL}{web3.to_hex(tx_hash)}"
        short_url = s0x999(tx_url)

        return {
            "tx_hash": web3.to_hex(tx_hash),
            "success": receipt.status == 1,
            "message": f"Add Liquidity {'(increase)' if existing_token_id else '(mint)'} | {amount0:.6f} {token0_symbol} + {amount1:.6f} {token1_symbol} | Tx: {short_url}"
        }

    except Exception as e:
        return {
            "tx_hash": None,
            "success": False,
            "message": f"❌ Add Liquidity failed: {str(e)}"
        }

def g0xprc3n(percent: float, token_symbol: str, parameters: dict) -> float:
    token_address_map = {
        "USDT": USDT_ADDRESS,
        "USDC": USDC_ADDRESS,
        "WPHRS": WPHRS_ADDRESS,
    }

    address = token_address_map.get(token_symbol)
    if not address:
        raise ValueError(f"Token symbol '{token_symbol}' tidak dikenali.")

    balance_str = check_balance({
        "provider": parameters["provider"],
        "privateKey": parameters["private_key"],
        "address": address
    })

    balance = Decimal(balance_str)
    amount = balance * Decimal(percent) / Decimal(100)
    return float(round(amount, 6))

def get_pool_price(web3, pool_address):
    pool = web3.eth.contract(address=pool_address, abi=UNISWAP_POOL_ABI)
    sqrt_price_x96 = pool.functions.slot0().call()[0]

    price = (Decimal(sqrt_price_x96) ** 2) / Decimal(2 ** 192)
    return float(round(price, 12))


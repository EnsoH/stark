import asyncio
import json
from loguru import logger
from starknet_py.net.full_node_client import FullNodeClient
from web3 import Web3
import random
from functools import wraps
from starknet_py.net.gateway_client import GatewayClient

from config import SETTINGS


def read_json(path):  # читает json abi
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as err:
        logger.error(f"Error -> {err}")


def read_wallets(path):  # читает приватники с тхт файла
    try:
        with open(path, "r") as file:
            return [line.strip() for line in file]
    except Exception as err:
        logger.error(f"Error -> {err}")


def random_int(min, max):  # генератор рандомного числа
    return random.randint(min, max)


def random_float(min, max):  # генератор рандомного числа
    return random.uniform(min, max)


async def sleep(min, max):  # функция для сна
    await asyncio.sleep(random_int(min, max))


async def check_gas():  # чекер газа
    try:
        client = GatewayClient("mainnet")
        # client = FullNodeClient(node_url=SETTINGS["RPC"])
        while True:
            block = await client.get_block("latest")
            gas = Web3.from_wei(block.gas_price, "gwei")
            if gas > SETTINGS["MAX_GAS"]:
                logger.warning(f'Gas is high now -> {gas:.2f} gwei')
                await asyncio.sleep(60, 120)
            else:
                break
    except Exception as err:
        logger.error(f"Error -> {err}")

# def gas_checker(func):
#     @wraps(func)
#     async def wrapped_func(*args, **kwargs):
#         try:
#             client = GatewayClient("mainnet")
#             while True:
#                 block = await client.get_block("latest")
#                 gas = Web3.from_wei(block.gas_price, "gwei")
#                 if gas > SETTINGS["MAX_GAS"]:
#                     logger.warning(f'Gas is high now -> {gas:.2f} gwei')
#                     await asyncio.sleep(60, 120)
#                 else:
#                     break
#             return await func(*args, **kwargs)
#         except Exception as err:
#             logger.error(f"Error -> {err}")
#
#     return wrapped_func


def retry(func):
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries < SETTINGS["RETRY_COUNT"]:
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error | {e}")
                await sleep(15, 60)
                retries += 1

    return wrapper



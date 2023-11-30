import asyncio

from starknet_py.contract import Contract
from web3 import Web3
from loguru import logger
import time

from common.constants import STARK_TOKENS, SITHSWAP_CON
from common.utils import read_json, random_float, retry, check_gas
from config import SETTINGS
from modules.client import Client


class SithSwap(Client):
    def __init__(self, private_key):
        super().__init__(private_key)

        abi = read_json("abis/sithswap_abi.json")
        self.contract = Contract(address=SITHSWAP_CON,
                                 abi=abi,
                                 provider=self.account)

    async def min_amount(self, amount, path):
        min_amount_data = await self.contract.functions["getAmountOut"].prepare(
            amount,
            path[0],
            path[1]
        ).call()

        return int(min_amount_data.amount - (min_amount_data.amount * SETTINGS["SLIPPAGE"])), min_amount_data.stable

    @retry
    async def swap_token_for_token(self, from_token, to_token):
        logger.debug("[SLEEP] Sleeping before module")
        await asyncio.sleep(SETTINGS["MIN_SLEEP"], SETTINGS["MAX_SLEEP"])
        await check_gas()

        logger.info(f"[SITHSWAP] MAKE SWAP TOKENS {from_token}->{to_token}")

        if from_token == "ETH":
            amount_random = random_float(SETTINGS["MIN_AMOUNT_ETH"], SETTINGS["MAX_AMOUNT_ETH"])
            amount_wei = Web3.to_wei(amount_random, "ether")
        else:
            abi = read_json("abis/stable_abi.json")
            contract = Contract(address=STARK_TOKENS["USDC"],
                                abi=abi,
                                provider=self.account)

            amount_data = await contract.functions["balanceOf"].call(self.address)
            amount_wei = amount_data.balance

        path = [STARK_TOKENS[from_token], STARK_TOKENS[to_token]]

        min_amount, stable = await self.min_amount(amount_wei, path)

        route = [{"from_address": path[0], "to_address": path[1], "stable": stable}]

        if from_token == "ETH":
            abi = read_json("abis/eth_abi.json")
        else:
            abi = read_json("abis/stable_abi.json")

        approve_con = Contract(address=STARK_TOKENS[from_token],
                               abi=abi,
                               provider=self.account)

        approve = approve_con.functions["approve"].prepare(
            SITHSWAP_CON,
            amount_wei
        )

        swap = self.contract.functions["swapExactTokensForTokensSupportingFeeOnTransferTokens"].prepare(
            amount_wei,
            min_amount,
            route,
            self.address,
            int(time.time()) + 1000000
        )

        resp = await self.account.execute(calls=[approve, swap], auto_estimate=True)
        await self.account.client.wait_for_tx(resp.transaction_hash)
        logger.success(f"[SITHSWAP] SUCCESSFULLY SWAP TOKENS {from_token}->{to_token} | "
                       f"https://starkscan.co/tx/{resp.transaction_hash}")

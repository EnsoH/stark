import asyncio

from starknet_py.contract import Contract
from starknet_py.net.client_models import Call

from loguru import logger
from starknet_py.hash.selector import get_selector_from_name

from common.constants import STARK_TOKENS, ZKLEND_CON
from common.utils import read_json, retry, check_gas
from config import ZKLEND_SETTINGS, SETTINGS
from modules.client import Client


class Zklend(Client):
    def __init__(self, private_key):
        super().__init__(private_key)

    @retry
    async def deposit(self):
        logger.debug("[SLEEP] Sleeping before module")
        await asyncio.sleep(SETTINGS["MIN_SLEEP"], SETTINGS["MAX_SLEEP"])
        await check_gas()

        logger.info(f"[ZKLEND] MAKE DEPOSIT ETH")

        amount_wei = int(await self.get_eth_amount() * ZKLEND_SETTINGS["dep_amount"])

        abi_eth = read_json("abis/eth_abi.json")
        contract_eth = Contract(address=STARK_TOKENS["ETH"],
                                abi=abi_eth,
                                provider=self.account)

        approve = contract_eth.functions["approve"].prepare(
            ZKLEND_CON["Router"],
            amount_wei
        )

        deposit = Call(
            to_addr=ZKLEND_CON["Router"],
            selector=get_selector_from_name("deposit"),
            calldata=[STARK_TOKENS["ETH"], amount_wei],
        )

        resp = await self.account.execute(calls=[approve, deposit], auto_estimate=True)
        await self.account.client.wait_for_tx(resp.transaction_hash)
        logger.success(f"[ZKLEND] DEPOSIT SUCCESSFULLY SENT -> https://starkscan.co/tx/{resp.transaction_hash}")

    @retry
    async def withdraw(self):
        logger.debug("[SLEEP] Sleeping before module")
        await asyncio.sleep(SETTINGS["MIN_SLEEP"], SETTINGS["MAX_SLEEP"])
        await check_gas()

        logger.info(f"[ZKLEND] MAKE WITHDRAW FROM LENDING")

        withdraw = Call(
            to_addr=ZKLEND_CON["Router"],
            selector=get_selector_from_name("withdraw_all"),
            calldata=[STARK_TOKENS["ETH"]],
        )

        resp = await self.account.execute(calls=[withdraw], auto_estimate=True)
        await self.account.client.wait_for_tx(resp.transaction_hash)
        logger.success(f"[ZKLEND] WITHDRAW SUCCESSFULLY GET -> https://starkscan.co/tx/{resp.transaction_hash}")

    @retry
    async def on_collateral(self):
        logger.debug("[SLEEP] Sleeping before module")
        await asyncio.sleep(SETTINGS["MIN_SLEEP"], SETTINGS["MAX_SLEEP"])
        await check_gas()

        logger.info(f"[ZKLEND] ENABLE COLLATERAL ON LENDING")

        collateral = Call(
            to_addr=ZKLEND_CON["Router"],
            selector=get_selector_from_name("enable_collateral"),
            calldata=[STARK_TOKENS["ETH"]],
        )

        resp = await self.account.execute(calls=[collateral], auto_estimate=True)
        await self.account.client.wait_for_tx(resp.transaction_hash)
        logger.success(f"[ZKLEND] SUCCESSFULLY ENABLING COLLATERAL -> https://starkscan.co/tx/{resp.transaction_hash}")

    @retry
    async def off_collateral(self):
        logger.debug("[SLEEP] Sleeping before module")
        await asyncio.sleep(SETTINGS["MIN_SLEEP"], SETTINGS["MAX_SLEEP"])
        await check_gas()

        logger.info(f"[ZKLEND] DISABLE COLLATERAL ON LENDING")

        collateral = Call(
            to_addr=ZKLEND_CON["Router"],
            selector=get_selector_from_name("disable_collateral"),
            calldata=[STARK_TOKENS["ETH"]],
        )

        resp = await self.account.execute(calls=[collateral], auto_estimate=True)
        await self.account.client.wait_for_tx(resp.transaction_hash)
        logger.success(f"[ZKLEND] SUCCESSFULLY DISABLING COLLATERAL -> https://starkscan.co/tx/{resp.transaction_hash}")

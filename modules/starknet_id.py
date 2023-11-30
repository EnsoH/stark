import asyncio

from starknet_py.net.client_models import Call
from loguru import logger
import random
from starknet_py.hash.selector import get_selector_from_name

from common.constants import STARKNET_ID
from common.utils import retry, check_gas
from config import SETTINGS
from modules.client import Client


class StarknedId(Client):
    def __init__(self, private_key):
        super().__init__(private_key)

    @retry
    async def mint_id(self):
        logger.debug("[SLEEP] Sleeping before module")
        await asyncio.sleep(SETTINGS["MIN_SLEEP"], SETTINGS["MAX_SLEEP"])
        await check_gas()

        logger.info("[STARKNET-ID] MAKE MINT ID")

        mint = Call(
            to_addr=STARKNET_ID,
            selector=get_selector_from_name("mint"),
            calldata=[int(random.random() * 1e12)],
        )

        resp = await self.account.execute(calls=[mint], auto_estimate=True)
        await self.account.client.wait_for_tx(resp.transaction_hash)
        logger.success(f"[STARKNET-ID] SUCCESSFULLY MINT ID https://starkscan.co/tx/{resp.transaction_hash}")

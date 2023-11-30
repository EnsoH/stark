import asyncio

from starknet_py.net.client_models import Call
from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from common.utils import retry, check_gas
from common.constants import STARKVERSE_CON
from config import SETTINGS
from modules.client import Client


class StarkVerse(Client):
    def __init__(self, private_key):
        super().__init__(private_key)

    @retry
    async def mint_nft(self):
        logger.debug("[SLEEP] Sleeping before module")
        await asyncio.sleep(SETTINGS["MIN_SLEEP"], SETTINGS["MAX_SLEEP"])
        await check_gas()

        logger.info("[STARKVERSE] MAKE MINT NFT")

        mint = Call(
            to_addr=STARKVERSE_CON,
            selector=get_selector_from_name("publicMint"),
            calldata=[self.address],
        )

        resp = await self.account.execute(calls=[mint], auto_estimate=True)
        await self.account.client.wait_for_tx(resp.transaction_hash)
        logger.success(f"[STARKVERSE] SUCCESSFULLY MINT NFT https://starkscan.co/tx/{resp.transaction_hash}")

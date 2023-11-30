import asyncio

from starknet_py.net.client_models import Call
from loguru import logger
import random
from hashlib import sha256
from starknet_py.hash.selector import get_selector_from_name
from common.utils import retry
from common.constants import STARKVERSE_CON
from config import SETTINGS
from modules.client import Client


class Dmail(Client):
    def __init__(self, private_key):
        super().__init__(private_key)

    @retry
    async def send_email(self):
        logger.debug("[SLEEP] Sleeping before module")
        await asyncio.sleep(SETTINGS["MIN_SLEEP"], SETTINGS["MAX_SLEEP"])

        logger.info("[DMAIL] SENDING EMAIL")

        email_address = sha256(str(1e10 * random.random()).encode()).hexdigest()
        theme = sha256(str(1e10 * random.random()).encode()).hexdigest()

        email_call = Call(
            to_addr=STARKVERSE_CON,
            selector=get_selector_from_name("transaction"),
            calldata=[email_address[0:31], theme[0:31]]
        )

        resp = await self.account.execute(calls=[email_call], auto_estimate=True)
        await self.account.client.wait_for_tx(resp.transaction_hash)
        logger.success(f"[DMAIL] SUCCESSFULLY SENT MAIL https://starkscan.co/tx/{resp.transaction_hash}")

import asyncio
import time
from web3 import Web3
from starknet_py.contract import Contract
from common.constants import STARK_TOKENS, SITHSWAP_CON
from starknet_py.net.client_models import Call
from loguru import logger
import random
from hashlib import sha256
from starknet_py.hash.selector import get_selector_from_name
from common.utils import retry, read_json
from common.constants import STARKVERSE_CON
from config import SETTINGS
from modules.client import Client


class Transfer(Client):
    def __init__(self, private_key):
        super().__init__(private_key)

    @retry
    async def send_transfer(self):
        logger.info("Make transfer to OKX ADDRESS")

        amount_to_trasnfer = 0.31 # ETH
        to_address = 0x06180b3ca893521b4c6df78832e240140217d4acc627155e78f249552d3d0941 # eth address

        amount_wei = Web3.to_wei(amount_to_trasnfer, "ether")

        abi = read_json("abis\eth_abi.json")
        contract = Contract(address=STARK_TOKENS["ETH"],
                               abi=abi,
                               provider=self.account)
    
        
        transfer_call = contract.functions["transfer"].prepare(to_address, amount_wei)
        resp = await self.account.execute(calls=[transfer_call], auto_estimate=True)
        await self.account.client.wait_for_tx(resp.transaction_hash)
        logger.success(f"[TX] SUCCESSFULLY TX https://starkscan.co/tx/{resp.transaction_hash}")
from starknet_py.hash import selector
from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.account.account import Account
from starknet_py.contract import Contract
from loguru import logger

from config import SETTINGS
from common.utils import read_json
from common.constants import (
    ARGENT_PROXY_CLASS_HASH,
    ARGENT_IMPLEMENTATION_CLASS_HASH,
    STARK_TOKENS,
    im_calss_hash_new
)


class Client:
    def __init__(self, private_key):
        self.client = FullNodeClient(node_url=SETTINGS["RPC"])
        self.key_pair = KeyPair.from_private_key(private_key)
        self.address = self.argent_address()
        self.account = Account(
            client=self.client,
            address=self.address,
            key_pair=self.key_pair,
            chain=StarknetChainId.MAINNET
        )

    def argent_address(self):
        address = compute_address(
            class_hash=im_calss_hash_new,
            constructor_calldata=[self.key_pair.public_key, 0],
            salt=self.key_pair.public_key,
        )

        return address

    async def get_eth_amount(self):
        abi = read_json("abis/eth_abi.json")
        contract = Contract(address=STARK_TOKENS["ETH"],
                            abi=abi,
                            provider=self.account)

        amount_data = await contract.functions["balanceOf"].call(self.address)

        return amount_data.balance

    async def deploy_account(self):
        logger.info(f"[DEPLOY] MAKING DEPLOY ACCOUNT")

        class_hash = 0x01a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003

        transaction = await self.account.deploy_account(
            address=self.address,
            class_hash=class_hash,
            salt=self.key_pair.public_key,
            key_pair=self.key_pair,
            client=self.client,
            chain=StarknetChainId.MAINNET,
            constructor_calldata=[self.key_pair.public_key, 0],
            auto_estimate=True
        )

        logger.success(f"[DEPLOY] DEPLOYED ACCOUNT -> https://starkscan.co/tx/")

import random

from common.utils import read_wallets
from config import ZKLEND_SETTINGS
from modules.dmail import Dmail
from modules.jediswap import JediSwap
from modules.sithswap import SithSwap
from modules.starknet_id import StarknedId
from modules.starkswap import TenSwap
from modules.starkverse import StarkVerse
from modules.zklend import Zklend
from modules.client import Client
from modules.transfer import Transfer


async def zklend():
    private_keys = read_wallets("user_data/private_keys")
    for private_key in private_keys:
        client = Zklend(private_key)
        await client.deposit()

        if random.random() < ZKLEND_SETTINGS["on_off_col"]:
            await client.on_collateral()
            await client.off_collateral()

        await client.withdraw()

async def jediswap():
    private_keys = read_wallets("user_data/private_keys")
    for private_key in private_keys:
        client = JediSwap(private_key)
        await client.swap_token_for_token("ETH", "USDC")
        await client.swap_token_for_token("USDC", "ETH")


async def starknet_id():
    private_keys = read_wallets("user_data/private_keys")
    for private_key in private_keys:
        client = StarknedId(private_key)
        await client.mint_id()


async def tenswap():
    private_keys = read_wallets("user_data/private_keys")
    for private_key in private_keys:
        client = TenSwap(private_key)
        await client.swap_token_for_token("ETH", "USDC")
        await client.swap_token_for_token("USDC", "ETH")


async def sith_swap():
    private_keys = read_wallets("user_data/private_keys")
    for private_key in private_keys:
        client = SithSwap(private_key)
        await client.swap_token_for_token("ETH", "USDC")
        await client.swap_token_for_token("USDC", "ETH")


async def starkverse():
    private_keys = read_wallets("user_data/private_keys")
    for private_key in private_keys:
        client = StarkVerse(private_key)
        await client.mint_nft()


async def dmail():
    private_keys = read_wallets("user_data/private_keys")
    for private_key in private_keys:
        client = Dmail(private_key)
        await client.send_email()


async def deploy():
    private_keys = read_wallets("user_data/private_keys")
    for private_key in private_keys:
        client = Client(private_key)
        await client.deploy_account()


async def txOkx():
    private_keys = read_wallets("user_data/private_keys")
    for private_key in private_keys:
        client = Transfer(private_key)
        await client.send_transfer()

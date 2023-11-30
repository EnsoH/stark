import asyncio
import random
from loguru import logger
from config import SETTINGS
from modules.tasks import zklend, jediswap, starknet_id, tenswap, sith_swap, starkverse, dmail


async def random_choice():
    func_weight = {
        zklend: 0.3,
        jediswap: 0.23333333333,
        starknet_id: 0.23333333333,
        tenswap: 0.23333333333,
        sith_swap: 0.23333333333,
    }
    num_transactions = random.randint(SETTINGS["MIN_TX"], SETTINGS["MAX_TX"])

    selected_functions = random.choices(list(func_weight.keys()), k=num_transactions,
                                        weights=list(func_weight.values()))

    # logger.debug(f"[RANDOM-MODULE] GENERATOR PATH -> {selected_functions}")
    print(f"Generator path - > {selected_functions}\n")
    # coroutines = [func() for func in selected_functions]
    # await asyncio.gather(*coroutines)

    for func in selected_functions:
        await func()

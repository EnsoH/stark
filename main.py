import asyncio
import colorama
from colorama import Fore

from modules.random_routes import random_choice
from modules.tasks import zklend, jediswap, starknet_id, tenswap, sith_swap, starkverse, dmail, deploy, txOkx

colorama.init(autoreset=True)


async def main():
    print(Fore.LIGHTRED_EX + """
  ____ _____  _    ____  _  ___   _ _____ _____ 
 / ___|_   _|/ \  |  _ \| |/ / \ | | ____|_   _|
 \___ \ | | / _ \ | |_) | ' /|  \| |  _|   | |  
  ___) || |/ ___ \|  _ <| . \| |\  | |___  | |  
 |____/ |_/_/   \_\_| \_\_|\_\_| \_|_____| |_|                                                                                                                                                    
""", Fore.YELLOW + "VERSION 1.0")

    print(Fore.LIGHTWHITE_EX +
          """
    Choose function to execute:""", Fore.LIGHTBLUE_EX + """
        ▫️ GENERATOR PATH(RANDOM MODULES) ➜ 0
        ▫️ ZKLEND(DEPOSIT/WITHDRAW/COLLATERA) ➜ 1
        ▫️ JEDISWAP(SWAP TOKENS) ➜ 2
        ▫️ STARKNET-ID(MINT ID) ➜ 3
        ▫️ 10KSWAP(SWAP TOKENS) ➜ 4
        ▫️ SITHSWAP(SWAP TOKENS) ➜ 5
        ▫️ STARKVERSE(MINT NFT) ➜ 6
        ▫️ DMAIL(SEND EMAIL) ➜ 7
        ▫️ DEPLOY() ➜ 8
        ▫️ Transfer() ➜ 9
    """)

    choice = input(Fore.LIGHTWHITE_EX + "    Enter number function: ")
    print()

    match choice:
        case "0":
            await random_choice()
        case "1":
            await zklend()
        case "2":
            await jediswap()
        case "3":
            await starknet_id()
        case "4":
            await tenswap()
        case "5":
            await sith_swap()
        case "6":
            await starkverse()
        case "7":
            pass
        case "8":
            await deploy()
        case "9":
            await txOkx()


if __name__ == "__main__":
    asyncio.run(main())

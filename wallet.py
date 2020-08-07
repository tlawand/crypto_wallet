import os, subprocess
import json
from constants import *

mnemonic = os.getenv('MNEMONIC','uncle eager comic achieve romance sun\
     sea spread nominee art rally comic')

num_keys = 3

def derive_wallets(mnemonic, coin, num_keys):
    output = subprocess.call(
        [
            './derive',
            f'--mnemonic={mnemonic}',
            f'--coin={coin}',
            f'--numderive={num_keys}',
            f'--format=json',
            '-g'
            ],
    )

    return output

coins = {
    BTCTEST: derive_wallets(mnemonic, BTCTEST, num_keys),
    ETH: derive_wallets(mnemonic, ETH, num_keys),
}

print(coins['btc-test'])
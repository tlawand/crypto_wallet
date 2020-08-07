import os, subprocess
import json
from constants import *

mnemonic = os.getenv('MNEMONIC','uncle eager comic achieve romance sun\
     sea spread nominee art rally comic')

num_keys = 3

def derive_wallets(mnemonic, coin, num_keys):
    p = subprocess.Popen(
        f'./derive --mnemonic="{mnemonic}" --coin={coin} --numderive={num_keys}\
             --format=json -g',
        stdout=subprocess.PIPE,
        shell=True
    )
    
    (output, err) = p.communicate()

    return json.loads(output)

coins = {
    BTCTEST: derive_wallets(mnemonic, BTCTEST, num_keys),
    ETH: derive_wallets(mnemonic, ETH, num_keys),
}

print(coins)
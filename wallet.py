import os, subprocess
import json
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from pprint import pprint
from constants import *

mnemonic = os.getenv('MNEMONIC','uncle eager comic achieve romance sun \
    sea spread nominee art rally comic')

num_keys = 3

def derive_wallets(mnemonic, coin, num_keys):
    p = subprocess.Popen(
        f'./derive -g --mnemonic="{mnemonic}" --coin={coin} \
            --numderive={num_keys} --format=json',
        stdout=subprocess.PIPE,
        shell=True
    )
    
    (output, _) = p.communicate()

    return json.loads(output)

# create a dictionary that derives 3 keys for each coin (BTC-Test & ETH)
coins = {
    BTCTEST: derive_wallets(mnemonic, BTCTEST, num_keys),
    ETH: derive_wallets(mnemonic, ETH, num_keys),
}

# using pprint (pretty print) instead of standard print to
# display output in a more readable format in the terminal
# uncomment to print coins object:
# pprint(coins) 

# test calling a child account from the coins dict
# print(f'{BTCTEST} key: {coins[BTCTEST][0]["privkey"]}')

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

def create_tx(coin, account, to, amount):
    if coin == ETH:
        gas_estimate = w3.eth.estimateGas(
            {'from': account.address, 'to': to, 'value': amount}
        )
        return {
            'to': to,
            'from': account.address,
            'value': amount,
            'gas': gas_estimate,
            'gasPrice': w3.eth.gasPrice,
            'nonce': w3.eth.getTransactionCount(account.address),
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(
            account.address,
            [(to, amount, BTC)]
            )

def send_tx(coin, account, to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(raw_tx)
    if coin == ETH:
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)
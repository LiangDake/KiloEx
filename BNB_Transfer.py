import json
import time

import web3
from web3.middleware import geth_poa_middleware


web3 = web3.Web3(web3.HTTPProvider("https://bsc-dataseed.binance.org/"))

# 连接公共节点需要注入此中间件
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

main_wallet_address = '0x830e6c22a45C409EC75cacB9F332E28D2fb605aA'
main_wallet_private_key = '7372838b2c867839b67d01a78e251cbcc754a97067e494ff399198105f75e823'


def multi_transfer(file_name):
    # 读取地址信息
    with open(file_name, 'r') as file:
        # 从文件中加载JSON数据
        wallet_dictionary = json.load(file)
        for wallet in wallet_dictionary:
            transfer_address = main_wallet_address
            # 接收钱包地址
            recipient = wallet['address']
            amount = web3.to_wei(0.006, 'ether')
            nonce = web3.eth.get_transaction_count(transfer_address)
            print(f"{transfer_address} 准备转账")

            transaction = {
                "from": transfer_address,
                "to": recipient,
                "value": amount,
                "gas": 250000,
                'gasPrice': web3.to_wei('5', 'gwei'),
                'nonce': nonce
            }

            # 私钥
            private_key = main_wallet_private_key
            signed_transcation = web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_transcation.rawTransaction)
            print(web3.to_hex(tx_hash))
            print(f"{transfer_address} 已转出 {amount} 个BNB")
            print()
            time.sleep(5)


multi_transfer('2024-1-12_mnemonic_address_bot.json')
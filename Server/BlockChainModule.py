from ethtoken.abi import EIP20_ABI
from web3 import Web3, HTTPProvider, IPCProvider

from Config import BLOCKCHAIN


class blockChain_connect():
    
    def __init__(self, provider = BLOCKCHAIN['node_provider'], contract_addr = BLOCKCHAIN['contract_address']):

        self.w3         = Web3(HTTPProvider(provider))
        self.contract   = self.w3.eth.contract(address=contract_addr, abi=EIP20_ABI)

    def get_balance(self, addr):
        return self.contract.functions.balanceOf(addr).call()

    def create_txn(self, addr_to, value, addr_from = BLOCKCHAIN['bank_address']['eth_address']):

        nonce        = self.w3.eth.getTransactionCount(addr_from)
        contract_txn = self.contract.functions.transfer(
            addr_to,
            value,
            ).buildTransaction({
                'chainId': BLOCKCHAIN['chain_id'],
                'gas': BLOCKCHAIN['gas'],
                'gasPrice': self.w3.toWei('1', 'gwei'),
                'nonce': nonce,
            })
        
        return contract_txn

    def sign_txn(self, txn, private_key = BLOCKCHAIN['bank_address']['private_key']):
        return self.w3.eth.account.signTransaction(txn, private_key=private_key)

    def send_txn(self, signed_txn):
        Hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return Web3.toHex(Hash)

    def master_txn_sender(self, addr_to, value):
        raw_txn     = self.create_txn(addr_to, value)
        signed_txn  = self.sign_txn(raw_txn)

        return self.send_txn(signed_txn)

import puurrtybot.api.blockfrost as blockfrost

import puurrtybot.functions as f
import os, puurrtybot, json, random

wallet_verify_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/verify_wallet"""


class WalletVerify:
    def __init__(self, userid: int, address: str = None, from_log: bool = False):
        self.address = address
        self.userid = userid
        self.log_path = f"""{wallet_verify_dir}/{self.userid}.json"""
        if from_log:
            self.read_log()
        else:
            self.new_verify()


    def read_log(self):
        with open(f"""{self.log_path}.json""", 'r') as json_file:
            log_data = json.load(json_file)
            if log_data['time'] + 1*1*60*60 - f.get_utc_time() > 0:
                self.address = log_data['address']
                self.stake_address = log_data['stake_address']
                self.address_list = log_data['address_list']
                self.amount = log_data['amount']
                self.userid = log_data['userid']
                self.time = log_data['time']
            else:
                self.delete_log()

    
    def create_log(self):
        with open(self.log_path, 'w') as json_file:
                json.dump({'address': self.address,
                           'stake_address' : self.stake_address,
                           'address_list' : self.address_list,
                           'amount' : self.amount,
                           'userid' : self.userid,
                           'time' : self.time}, json_file)


    def delete_log(self):
        os.unlink(self.log_path)


    def new_verify(self):
        self.stake_address = blockfrost.get_stake_address_by_address(self.address)
        self.address_list = blockfrost.get_address_list_by_stake_address(self.stake_address)
        self.amount = str(random.choice(list(range(2_000_000, 3_000_000+1))))
        self.userid = self.userid
        self.time = f.get_utc_time()
        self.create_log()

        
    def verify_transaction(self):
        self.tx_hash_list = blockfrost.get_tx_hash_list_by_address(self.address)
        for tx_hash in self.tx_hash_list:
            utxo_list = blockfrost.get_utxo_list_by_tx_hash(tx_hash)
            utxo_list = blockfrost.get_utxo_list_by_tx_hash(tx_hash)
            for utxo_input in utxo_list['inputs']:
                if utxo_input['address'] not in self.address_list:
                    return False
            for utxo_output in utxo_list['outputs']:
                if utxo_output['address'] == self.address and self.amount in [entry['quantity'] for entry in utxo_output['amount']]:
                    self.delete_log()
                    return True
        return False


def get_interrupted_verification():
    return os.listdir(wallet_verify_dir)
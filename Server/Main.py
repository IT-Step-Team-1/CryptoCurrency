
from time import sleep
from BlockChainModule import blockChain_connect
from LogModule import Logging
from RequestModule import API
from MainConfig import API_Settings, BLOCKCHAIN

global log

log = Logging()
log.info('Starting Mainloop')

blockchain = blockChain_connect()

while True:

    data = API().getTransactions()

    if data == 'NONE':
        log.warning('[API().getTransactions] Returns NONE')
        log.info('Sleep 30 sec')

        sleep(30)
        continue
    
    elif data == 'ERROR':
        log.error('[API().getTransactions()] Returns ERROR')
        log.info('Sleep 30 sec')

        sleep(30)
        continue

    else:
        log.info('[API().getTransactions] Returned json structure')

        data_len = len(data['data'])

        log.info('Json structure length is {}'.format(str(data_len)))
        log.info('Starting search in json structure Status: 0')
        for i in data['data']:

            if data['data'][str(i)]['Status'] == '1':
                continue

            else:
                txn_id          = str(i)
                txn_ETH_address = str(data['data'][txn_id]['ETH_Address'])
                txn_Value       = data['data'][txn_id]['Value']

                log.warning('Found txn with Status: 0')
                log.info('Txn ID: {}'.format(str(txn_id)))
                log.info('Txn ETH Address: {}'.format(txn_ETH_address))
                log.info('Txn Value: {}'.format(str(txn_Value)))

                log.info('[BlockChain] Checking balance {}'.format(BLOCKCHAIN['bank_address']['eth_address']))

                eth_balance = blockchain.get_balance(BLOCKCHAIN['bank_address']['eth_address'])

                if eth_balance < int(txn_Value):
                    log.error('[BlockChain] Not enough tokens, balance is {} need {}'.format(str(eth_balance), str(txn_Value)))
                    log.info('Exit')

                    exit()
                else:
                    log.info('[BlockChain] Enough tokens, balance is {} need {}'.format(str(eth_balance), str(txn_Value)))


                log.warning('[BlockChain] Creating Transaction  Id: {}; To: {}; Value: {}'.format(str(txn_id), txn_ETH_address, str(txn_Value)))

                contract_txn    = blockchain.create_txn(txn_ETH_address, int(txn_Value))

                log.info('[BlockChain] Transaction Created, Id: {}'.format(str(txn_id)))


                log.warning('[BlockChain] Signing Transaction, Id: {}'.format(str(txn_id)))

                signed_txn      = blockchain.sign_txn(contract_txn)

                log.info('[BlockChain] Transaction Singing Successful, Id: {}'.format(str(txn_id)))


                log.warning('[BlockChain] Sending Transaction in BlockChain, Id: {}'.format(str(txn_id)))

                txn_hash        = blockchain.send_txn(signed_txn)

                log.info('[BlockChain] Transaction Successfuly Sended Hash: {}'.format(txn_hash))


                log.warning('Changing transaction Status in DB, Id: {}'.format(str(txn_id)))

                status = API().ChangeStatus(txn_id)

                if status['status'] == 'ERROR':
                    log.error('Cant Change Status in DB, Id: {}'.format(str(txn_id)))
                    log.info('Exit')

                    exit()

                elif status['status'] == 'DONE':
                    log.info('Successfuly Changing Status in DB, Id: {}'.format(str(txn_id)))

                log.info('Transaction with Id: {} successfuly processed'.format(str(txn_id)))

        log.info('Sleep 100 sec')
        sleep(100)
        continue

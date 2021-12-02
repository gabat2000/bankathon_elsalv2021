#BITCOIN
from bitcoinlib.wallets import Wallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.services.services import Service
#DB
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
#FLASK
from flask import request
from flask import Flask
from flask_cors import CORS
#GENERAL
import os
import requests
import json
from flask import jsonify
#LOG
import logging
from logging.handlers import RotatingFileHandler
#SECURITY
from cryptography.fernet import Fernet

#DB Variable
db_domain, db_sec = "db.us.fauna.com", "fnAEYw6bk-AARKp5NX2OvoQuTByJVgJ9RvugkZmF"
#IPs allowed
trustedIpList=["52.89.214.238","34.212.75.30","54.218.53.128","52.32.178.7","127.0.0.1","174.93.244.121"]
#Log file
logger = logging.getLogger('WALLET')
#hdlr = logging.FileHandler('log/med.log')
hdlr = RotatingFileHandler("log/wallet.log", maxBytes=2000000, backupCount=200)
#hdlr = RotatingFileHandler("log/mmt.log", maxBytes=20000, backupCount=200)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)
logger.info('<<----------------------------------------------------->>')
logger.info(" WALLET Log start \n")

#APP
app = Flask(__name__)
if __name__ == "__main__":
    app.run(ssl_context='adhoc')
CORS(app)

@app.route('/')
def hello_med():
    return 'Hello, WALLET!'

@app.route('/wallet/create/', methods=['GET', 'POST'])
def txExecutionCreate():
    originT = originTrusted(request.remote_addr)
    #if originT == False: 
    #    logger.critical('[WALLET][REQUEST][IP ORIGIN] denied with ip: %s' % str(originT))
    #    return ''
    logger.info('[MAIN][CREATE][REQUEST][IP ORIGIN] allowed with ip: %s' % str(request.remote_addr))
    try:
        if request.method == 'GET':
            username, password = request.args.get('username'), request.args.get('password')
            if username == 'ping': return "ping"
            #PING
            logger.info('-----------[CREATE][INICIANDO GET]-----------')
            return ''
        if request.method == 'POST':
            logger.info(" ------------------[CREATE][INICIANDO POST]-------------------- \n")
            #Datos del request
            username, password = request.args.get('username'), request.args.get('password')
            data = request.get_data()
            dataContent=data.decode('utf-8')
            logger.info('[MAIN][CREATE][MESSAGE] Content: %s' % (str(dataContent)))
            w_request_text = str(dataContent)
            if w_request_text is None:
                return jsonify({"message":"text not found"})
            logger.info('[MAIN][CREATE][JSON] '+w_request_text)
            w_request_dict = json.loads(w_request_text)
            w_network, w_name, w_account = w_request_dict['wallet']['network'], w_request_dict['wallet']['name'], w_request_dict['wallet']['account']
            # creado cuenta
            wallet_info = create_wallet(w_network,w_name,w_account)
            wallet_w_dict, numo_w = wallet_info[0], wallet_info[1]
            if wallet_w_dict is None: return jsonify({"message":"wallet is None"})
            wallet_w_dict["numonic"] = numo_w 
            json_object = json.dumps(str(wallet_w_dict))
            logger.info('[MAIN][CREATE][END JSON] ')        
            return json_object
    except Exception as err:
        print('[MAIN][CREATE][GENERAL] Error gettingith response:, error: {0}'.format(str(err)))
        logger.error('[MAIN][CREATE][GENERAL] Error getting response , error: {0}'.format(err))
        logger.exception(err)
    return jsonify({"message":"can not be created"})

@app.route('/wallet/balance/', methods=['GET'])
def txExecutionBalance():
    originT = originTrusted(request.remote_addr)
    #if originT == False: 
    #    logger.critical('[WALLET][REQUEST][IP ORIGIN] denied with ip: %s' % str(originT))
    #    return ''
    logger.info('[MAIN][BALANCE][REQUEST][IP ORIGIN] allowed with ip: %s' % str(request.remote_addr))
    try:
        if request.method == 'GET':
            username, password = request.args.get('username'), request.args.get('password')
            if username == 'ping': return "ping"
            #PING
            logger.info('-----------[BALANCE][INICIANDO GET]-----------')
            data = request.get_data()
            dataContent=data.decode('utf-8')
            logger.info('[MAIN][BALANCE][MESSAGE] Content: %s' % (str(dataContent)))
            w_request_text = str(dataContent)
            if w_request_text is None:
                return jsonify({"message":"text not found"})
            logger.info('[MAIN][BALANCE][JSON] '+w_request_text)
            w_request_dict = json.loads(w_request_text)
            w_network, w_name, w_account = w_request_dict['wallet']['network'], w_request_dict['wallet']['name'], w_request_dict['wallet']['account']
            w = Wallet(w_name)
            logger.info('[MAIN][BALANCE] to get balance')
            balance_s = w.balance_update_from_serviceprovider()/100000000
            w.scan()
            balance = w.balance(0,w_network,False)/100000000
            balance_str = w.balance(0,w_network,True)
            balance_dict={}
            balance_dict['balance_s'], balance_dict['balance'], balance_dict['balance_str'], balance_dict['wallet_address'] = format(balance_s,'.8f'), format(balance,'.8f'), balance_str, w.addresslist()[0]
            logger.info('[MAIN][BALANCE][END JSON]')
            json_object = json.dumps(str(balance_dict))
            return json_object
    except Exception as err:
        print('[MAIN][BALANCE][GENERAL] Error gettingith response:, error: {0}'.format(str(err)))
        logger.error('[MAIN][BALANCE][GENERAL] Error getting response , error: {0}'.format(err))
        logger.exception(err)
    return jsonify({"message":"can not get info"})

@app.route('/wallet/send/', methods=['POST'])
def txExecutionSend():
    originT = originTrusted(request.remote_addr)
    #if originT == False: 
    #    logger.critical('[WALLET][REQUEST][IP ORIGIN] denied with ip: %s' % str(originT))
    #    return ''
    logger.info('[MAIN][SEND][REQUEST][IP ORIGIN] allowed with ip: %s' % str(request.remote_addr))
    try:
        if request.method == 'POST':
            username, password = request.args.get('username'), request.args.get('password')
            if username == 'ping': return "ping"
            #PING
            logger.info('-----------[SEND][INICIANDO POST]-----------')
            data = request.get_data()
            dataContent=data.decode('utf-8')
            logger.info('[MAIN][SEND][MESSAGE] Content: %s' % (str(dataContent)))
            w_request_text = str(dataContent)
            if w_request_text is None:
                return jsonify({"message":"text not found"})
            logger.info('[MAIN][SEND][JSON]')
            w_request_dict = json.loads(w_request_text)
            w_network, w_name, w_account = w_request_dict['wallet']['network'], w_request_dict['wallet']['name'], w_request_dict['wallet']['account']
            address_destination, amount = w_request_dict['address_destination'], float(w_request_dict['amount'])*100000000
            w = Wallet(w_name)
            logger.info('[MAIN][SEND] to get balance')
            balance_s = (w.balance_update_from_serviceprovider())
            w.scan()
            balance, balance_str = w.balance(0,w_network,False), w.balance(0,w_network,True)
            tx = None
            logger.info('[MAIN][SEND][BALANCE] BAL:'+ format(balance,'.8f')+' - STR:'+balance_str +' - PROVIDERS:'+format(balance_s,'.8f'))
            if balance_s > amount:
                try:
                    tx=w.send_to(address_destination, amount)
                except Exception as error:
                    logger.error('[MAIN][SEND][ENVIO] Error enviando , error: {0}'.format(error))
                    logger.exception(error)
                try:
                    if tx is not None:
                        tx_dict = tx.as_dict()
                        tx_dict['balance_s'], tx_dict['balance'], tx_dict['balance_str'], tx_dict['origin_address'], tx_dict['amount_sent'] =format(balance_s/100000000,'.8f'), format(balance/100000000,'.8f'), balance_str, w.addresslist()[0], format(amount/100000000,'.8f')
                        db_client = get_db_client()
                        db_client.query(q.create(q.collection('transacciones'), {"data":tx_dict}))
                        logger.info('[FNT][CREATE WALLET][GUARDADA] ')
                        json_object = json.dumps(str(tx_dict))
                        return json_object
                except Exception as error:
                    logger.error('[MAIN][SEND][GUARDANDO TX] Error al guardar tx , error: {0}'.format(error))
                    logger.exception(error)    
            else:
                return jsonify({"message":"balance is not enough"+str(balance_s)})
            logger.info('[MAIN][SEND][END JSON]')
            return jsonify({"message":"Tx not finished"})
    except Exception as err:
        print('[MAIN][SEND][GENERAL] Error gettingith response:, error: {0}'.format(str(err)))
        logger.error('[MAIN][SEND][GENERAL] Error getting response , error: {0}'.format(err))
        logger.exception(err)
    return jsonify({"message":"can not get info"})

def originTrusted(origin_ip):
    for trustedIp in trustedIpList:
        if str(origin_ip) == trustedIp: originTrusted = True
    return True

def get_db_client():
    db_client = FaunaClient(secret=db_sec, domain=db_domain, port=443, scheme="https")
    return db_client

def create_wallet_chain(network,w_name,btc_name):
    try:
        passphrase = Mnemonic().generate()
        #print("NEMONICS: "+str(passphrase))
        w = Wallet.create(w_name, keys=passphrase, network=network)
        account_btc2 = w.new_account(btc_name)
        #account_ltc1 = w.new_account('Account LTC', network='litecoin')
        w_key1=w.get_key()
        #print("LLAVE: "+str(w_key1))
        w.get_key(account_btc2.account_id)
        #w.get_key(account_ltc1.account_id)
        #w.info()
        return [w, passphrase]
    except Exception as err:
        print('[FNT][CREATE WALLET CHAIN] Error creando billetera en cadena, error: {0}'.format(str(err)))
        logger.error('[FNT][CREATE WALLET CHAIN] Error creado billetera en cadena, error: {0}'.format(err))
        logger.exception(err)
    return None

def print_db_info(db_client):
    indexes = db_client.query(q.paginate(q.indexes()))
    coll = db_client.query(q.paginate(q.collections()))
    print(coll)
    print(indexes)

def create_wallet(network,wallet_name,account_name):
    try:
        db_client = get_db_client()
        wallet_data = create_wallet_chain(network,wallet_name,account_name)
        wallet_w = wallet_data[0]
        numo_w = wallet_data[1]
        w_id, w_name,w_wif,w_network, w_pwif =wallet_w.wallet_id, wallet_w._name,wallet_w.get_keys()[0].wif,wallet_w.network_list()[0], wallet_w.public_master().wif
        w_add1, w_add2, w_add3 = wallet_w.keys_addresses()[0].address, wallet_w.keys_addresses()[1].address, wallet_w.keys_addresses()[2].address
        wallet_w_dict = wallet_w.as_dict()
        logger.info('[FNT][CREATE WALLET][CREADA] '+str(wallet_w_dict))
        db_client.query(q.create(q.collection('wallets'), {"data":wallet_w_dict}))
        logger.info('[FNT][CREATE WALLET][GUARDADA] ')
        return [wallet_w_dict,numo_w]
    except Exception as err:
        print('[FNT][CREATE WALLET] Error creando billetera, error: {0}'.format(str(err)))
        logger.error('[FNT][CREATE WALLET] Error creado billetera, error: {0}'.format(err))
    return None


#t=wallet_w.send_to('n1SvLt9ujMjpPSzKG56ttsw3VxDzaWctcZ', 1000)

#w.scan()
#w.info()  # Shows wallet information, keys, transactions and UTXO's
#tx_id = t = w.send_to(w_key1, '0.001 BTC')
#print("TX ID: "+tx_id)
#t.info  # Shows transaction information and send results

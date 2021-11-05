import os
import logging
import lnd_grpc
from flask_cors import CORS, cross_origin
from flask import request, Flask
from decouple import config
# import lnurl

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())
APP_DIR = os.path.dirname(__file__)
app = Flask('app', static_folder=os.path.join(APP_DIR, 'static'), static_url_path='/static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
lnd_rpc = lnd_grpc.Lightning(
            lnd_dir=config('lnd_dir'),
            macaroon_path=config('macaroon_path'),
            tls_cert_path=config('tls_cert_path'),
            network='mainnet',
            grpc_host='localhost',
            grpc_port='10009')


@app.route("/invoice/", methods=['POST'])
@cross_origin()
def add():
    request_data = request.get_json()
    value = request_data['amount']
    print(value)
    value = max(min(int(value), 17000), 100)
    res = lnd_rpc.add_invoice(value=value)
    print(res)
    return {'payment_request': res.payment_request, 'add_index': res.add_index}


@app.route("/invoice/<add_index>", methods=['GET'])
@cross_origin()
def settled_by_index(add_index):
    for invoice in lnd_rpc.subscribe_invoices():
        print('state:', invoice.state)
        print('index:', invoice.add_index)
        if invoice.state == 1 and invoice.add_index == int(add_index):
            return {'settled': invoice.state}
    return {'settled': 0}


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    with open(os.path.join(APP_DIR, 'static/qr.html')) as f:
        return f.read()

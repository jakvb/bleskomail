import logging
import lnd_grpc
from flask import request, Response, Flask
from decouple import config
# import lnurl
import os

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

app = Flask('app')
lnd_rpc = lnd_grpc.Lightning(
            lnd_dir=config('lnd_dir'),
            macaroon_path=config('macaroon_path'),
            tls_cert_path=config('tls_cert_path'),
            network='mainnet',
            grpc_host='localhost',
            grpc_port='10009')


@app.route("/invoice", methods=['POST'])
def add():
    request_data = request.get_json()
    value = request_data['value']
    value = max(min(int(value), 5000), 100)
    res = lnd_rpc.add_invoice(value=value)
    print(res)
    return {'payment_request': res.payment_request, 'add_index': res.add_index}


@app.route("/invoice/<add_index>", methods=['GET'])
def settled_by_index(add_index):
    for invoice in lnd_rpc.subscribe_invoices():
        print(invoice)
        print('state:' + invoice.state)
        print('index:' + invoice.add_index)
        if invoice.state == 'SETTLED' and invoice.add_index == add_index:
            return {'settled': 1}
    return {'settled': 0}


@app.route("/", methods=['GET'])
def home():
    with open(os.path.join(os.path.dirname(__file__), 'qr.html')) as f:
        return f.read()

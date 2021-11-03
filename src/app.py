import logging
import lnd_grpc
from flask import request, Response, Flask
from decouple import config
# import lnurl

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


@app.route("/invoice/add", methods=['POST'])
def add():
    request_data = request.get_json()
    value = request_data['value']
    value = max(min(int(value), 5000), 100)
    res = lnd_rpc.add_invoice(value=value)
    print(res)
    return res.payment_request


from flask import Flask
import lnd_grpc
from decouple import config
# import lnurl

lnd_rpc = lnd_grpc.Lightning(
            lnd_dir=config('lnd_dir'),
            macaroon_path=config('macaroon_path'),
            tls_cert_path=config('tls_cert_path'),
            network='mainnet',
            grpc_host='localhost',
            grpc_port='10009')
res = lnd_rpc.add_invoice(value=100)
print(res)
print(type(res))
print(dict(res))
app = Flask('app')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.request_options import RequestOptions
from config import config
import json

username = config['sp_user']
password = config['sp_password']
url = config['sp_base_path']
client_id = config['sp_client_id']
client_secret = config['sp_client_secret']

ctx_auth = AuthenticationContext(url)
if ctx_auth.acquire_token_for_app(client_id, client_secret):
    request = ClientRequest(ctx_auth)
    options = RequestOptions("{0}/_api/web/lists/GetByTitle('Area')/items".format(url))
    options.set_header('Accept', 'application/json')
    options.set_header('Content-Type', 'application/json')
    data = request.execute_request_direct(options)
    s = json.loads(data.content)
    print(s)
else:
    print(ctx_auth.get_last_error())

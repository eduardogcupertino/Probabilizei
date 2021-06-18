from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.request_options import RequestOptions
import json


from config import config

url = 'https://gruposimbio.sharepoint.com/sites/dev'
username = config['sp_user']
password = config['sp_password']

ctx_auth = AuthenticationContext(url)
if ctx_auth.acquire_token_for_user(username, password):
    ctx = ClientContext(url, ctx_auth)
    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    print("Web title: {0}".format(web.properties['Title']))
else:
    print(ctx_auth.get_last_error())
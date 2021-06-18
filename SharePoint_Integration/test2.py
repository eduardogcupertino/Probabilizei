import requests
from shareplum import Office365

# Obtain auth cookie
authcookie = Office365('https://gruposimbio.sharepoint.com/sites/dev', username='eduardo.silva@simbiox.com.br',password='Robotics01').GetCookies()
session = requests.Session()
session.cookies = authcookie
session.headers.update({'user-agent': 'python_bite/v1'})
session.headers.update({'accept': 'application/json;odata=verbose'})
import os
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.request_options import RequestOptions
import json
from office365.sharepoint.file_creation_information import FileCreationInformation

from config import config

url = 'https://gruposimbio.sharepoint.com/sites/dev'
username = config['sp_user']
password = config['sp_password']
path = r'C:\Users\gamac\Desktop\Projects\SharePoint_Integration\test.txt'

ctx_auth = AuthenticationContext(url)

ctx = ClientContext(url, ctx_auth)

with open(path, 'rb') as content_file:
    file_content = content_file.read()

list_title = "NovaBiblioteca"
target_folder = ctx.web.lists.get_by_title(list_title).rootFolder
name = os.path.basename(path)
target_file = target_folder.upload_file(name, file_content)
ctx.execute_query()
print("File url: {0}".format(target_file.serverRelativeUrl))

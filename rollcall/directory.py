import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run


def directory_service():
    """Instantiate a Google API directory service object."""
    flow = flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/admin.directory.group.readonly https://www.googleapis.com/auth/admin.directory.user.readonly',
        message='oops',
    )
    storage = Storage('tokens.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run(flow, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('admin', 'directory_v1', http=http)
    return service

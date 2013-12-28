import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

from django.core.management.base import BaseCommand

from rollcall.people.models import Person



class Command(BaseCommand):
    args = 'args'
    help = 'help'

    def handle(self, *args, **options):
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

        fetch_more = True
        page_token = None
        while fetch_more:
            list_people = service.users().list(
                    domain='digital.cabinet-office.gov.uk',
                    pageToken=page_token,
                ).execute()

            page_token = list_people.get('nextPageToken', None)
            if page_token is None:
                fetch_more = False

            for item in list_people['users']:
                person, created = Person.objects.get_or_create(
                    name = item['name']['fullName'],
                    email = item['primaryEmail'],
                    google_id = item['id'],
                )
                if created:
                    person.save()
                    print 'Added %s <%s>' % ( person.name, person.email )

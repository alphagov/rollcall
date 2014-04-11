import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

from django.core.management.base import BaseCommand

from rollcall.directory import directory_service
from rollcall.people.models import Person



class Command(BaseCommand):
    args = 'args'
    help = 'help'

    def handle(self, *args, **options):
        service = directory_service()

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

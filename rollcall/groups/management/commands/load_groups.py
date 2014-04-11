import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

from django.core.management.base import BaseCommand

from rollcall.groups.models import Group
from rollcall.people.models import Person
from rollcall.directory import directory_service



class Command(BaseCommand):
    args = 'args'
    help = 'help'

    def handle(self, *args, **options):
        service = directory_service()

        fetch_more = True
        page_token = None
        while fetch_more:
            list_groups = service.groups().list(
                    domain = 'digital.cabinet-office.gov.uk',
                    pageToken = page_token,
                ).execute()

            page_token = list_groups.get('nextPageToken', None)
            if page_token is None:
                fetch_more = False

            for item in list_groups['groups']:
                group, created = Group.objects.get_or_create(
                    name = item['name'],
                    email = item['email'],
                    description = item['description'],
                )
                if created:
                    group.save()
                    print 'Added', item['name']

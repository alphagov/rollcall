import httplib2

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

from django.core.management.base import BaseCommand, CommandError

from rollcall.groups.models import Group, Membership
from rollcall.people.models import Person
from rollcall.directory import directory_service



class Command(BaseCommand):
    args = 'args'
    help = 'help'

    def handle(self, *args, **options):
        service = directory_service()

        groups = Group.objects.all()
        for group in groups:
            fetch_more = True
            page_token = None
            while fetch_more:
                memberships = service.members().list(
                        groupKey=group.email,
                        pageToken = page_token,
                    ).execute()

                page_token = memberships.get('nextPageToken', None)
                if page_token is None:
                    fetch_more = False

                has_members = memberships.get('members')
                if not has_members:
                    continue
                
                for member in memberships['members']:
                    try:
                        person = Person.objects.get(email=member['email'])
                        membership, created = Membership.objects.get_or_create(
                            person=person,
                            group=group,
                            role=member['role'],
                        )
                        if created:
                            print 'Added %s to %s' % ( person, group )
                    except Person.DoesNotExist:
                        try:
                            sublist = Group.objects.get(email=member['email'])
                            group.sublists.add(sublist)
                            print 'Added sublist %s to %s' % ( sublist, group )
                        except Group.DoesNotExist:
                            # not a GDS email
                            pass

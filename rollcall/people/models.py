from hashlib import md5

from django.db import models

from autoslug import AutoSlugField



class Person(models.Model):
    class Meta:
        verbose_name_plural = 'people'

    name = models.CharField( max_length=256 )
    email = models.CharField( max_length=256, unique=True )
    google_id = models.CharField( max_length=64 )
    slug = AutoSlugField( populate_from='name', unique=True )

    @property
    def avatar_url(self):
        return 'http://gravatar.com/avatar/%s' % md5(self.email).hexdigest()

    def manager(self):
        for membership in self.memberships_as_member():
            if membership.group.email.find('gds-reports') == 0:
                first_owner = membership.group.owners()[0]
                return first_owner.person
        return None

    def manages(self):
        manages = []
        for membership in self.memberships_as_owner():
            if membership.group.email.find('gds-reports') == 0:
                for list_member in membership.group.membership_set.filter(role='MEMBER'):
                    manages.append(list_member.person)
        return manages

    def roles(self):
        from rollcall.groups.models import GroupState

        memberships = self.membership_set.filter(
            group__state=GroupState.format_one,
            group__list_type='members',
            group__subject_type='role'
        )
        return map(lambda m: m.group, memberships)

    def teams(self):
        from rollcall.groups.models import GroupState

        memberships = self.membership_set.filter(
            group__state=GroupState.format_one,
            group__list_type='members',
            group__subject_type='team'
        )
        return map(lambda m: m.group, memberships)

    @property
    def clan(self):
        for membership in self.membership_set.all():
            if membership.group.email.find('gds-clan') == 0:
                return membership.group.name

    @property
    def is_head_of_clan(self):
        for membership in self.memberships_as_owner():
            if membership.group.email.find('gds-clan') == 0:
                return True
        return False

    def memberships(self):
        return self.membership_set.all()

    def memberships_as_member(self):
        return self.membership_set.filter(role='MEMBER')

    def memberships_as_owner(self):
        return self.membership_set.filter(role='OWNER')

    def __unicode__(self):
        return self.name

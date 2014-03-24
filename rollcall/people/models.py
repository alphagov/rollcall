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

    def membership_by_type(self, subject_type, list_type='members', area=None, role=None):
        from rollcall.groups.models import GroupState

        filter = {
            'group__state': GroupState.format_one,
            'group__list_type': list_type,
            'group__subject_type': subject_type,
        }
        if area is not None:
            filter['group__area'] = area
        if role is not None:
            filter['role'] = role
        return self.membership_set.filter(**filter)

    def manager(self):
        list = self.membership_by_type('reports', role='MEMBER')
        if list:
            return list[0].group.owners()[0].person
        return None

    def manages(self):
        list = self.membership_by_type('reports', role='OWNER')
        if list:
            membership = list[0].group.membership_set.filter(role='MEMBER')
            return map(lambda m: m.person, membership)
        return None

    def roles(self):
        memberships = self.membership_by_type('role')
        return map(lambda m: m.group, memberships)

    def teams(self):
        memberships = self.membership_by_type('team')
        return map(lambda m: m.group, memberships)

    def subscribed_topics(self):
        memberships = self.membership_by_type('topic', 'discuss')
        return map(lambda m: m.group, memberships)

    @property
    def clan(self):
        list = self.membership_by_type('clan', area='gds')
        if list:
            return list[0].group.name
        return None

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

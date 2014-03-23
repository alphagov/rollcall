import re

from django.db import models
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField
from dj.choices import Choices, Choice
from dj.choices.fields import ChoiceField

from rollcall.people.models import Person



class GroupState(Choices):
    unknown = Choice('Unknown: investigate')
    known = Choice('Known')
    old_format = Choice('Old format: should be migrated')
    format_one = Choice('New format')


class Group(models.Model):
    QUAD_FORMAT_PATTERN = re.compile(
        """
            ^
                (?P<area> # which functional area, or 'gds' for all
                    gds | govuk | pdu | transformation
                )
            -
                (?P<subject_type> # eg team, role, topic, repo, contact
                    [a-z0-9]+
                )
            -
                (?P<subject> # the team, role, etc
                    [a-z0-9-]+
                )
            -
                (?P<list_type>
                    announce | discuss | members
                )
            @
        """,
        re.IGNORECASE | re.VERBOSE
    )

    name = models.CharField( max_length=256 )
    email = models.CharField( max_length=256 )
    description = models.CharField( max_length=256 )
    slug = AutoSlugField( populate_from='name', unique=True )

    # memberships
    members = models.ManyToManyField( Person, through='Membership' )
    sublists = models.ManyToManyField( 'self', symmetrical=False, blank=True, null=True )

    # state
    state = ChoiceField( choices=GroupState, default=GroupState.unknown )
    area = models.CharField( max_length=256, blank=True, null=True )
    subject_type = models.CharField( max_length=256, blank=True, null=True )
    subject = models.CharField( max_length=256, blank=True, null=True )
    list_type = models.CharField( max_length=256, blank=True, null=True )

    def owners(self):
        return self.membership_set.filter(role='OWNER')

    def get_absolute_url(self):
        return reverse( 'group-detail', kwargs={ 'slug': self.slug } )

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        quads = self.QUAD_FORMAT_PATTERN.match(self.email)
        if quads is not None:
            self.state = GroupState.format_one
            self.area = quads.group('area')
            self.subject_type = quads.group('subject_type')
            self.subject = quads.group('subject')
            self.list_type = quads.group('list_type')
        super(Group, self).save(*args, **kwargs)


class Membership(models.Model):
    group = models.ForeignKey(Group)
    person = models.ForeignKey(Person)
    role = models.CharField( max_length=64 )

    def __unicode__(self):
        return u'%s in %s' % ( self.person, self.group )

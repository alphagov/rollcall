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
    name = models.CharField( max_length=256 )
    email = models.CharField( max_length=256 )
    description = models.CharField( max_length=256 )
    slug = AutoSlugField( populate_from='name', unique=True )

    # memberships
    members = models.ManyToManyField( Person, through='Membership' )
    sublists = models.ManyToManyField( 'self', symmetrical=False, blank=True, null=True )

    # state
    state = ChoiceField( choices=GroupState, default=GroupState.unknown )

    def owners(self):
        return self.membership_set.filter(role='OWNER')

    def get_absolute_url(self):
        return reverse( 'group-detail', kwargs={ 'slug': self.slug } )

    def __unicode__(self):
        return self.email


class Membership(models.Model):
    group = models.ForeignKey(Group)
    person = models.ForeignKey(Person)
    role = models.CharField( max_length=64 )

    def __unicode__(self):
        return u'%s in %s' % ( self.person, self.group )

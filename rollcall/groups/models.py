from django.db import models

from autoslug import AutoSlugField

from rollcall.people.models import Person



class Group(models.Model):
    name = models.CharField( max_length=256 )
    email = models.CharField( max_length=256 )
    description = models.CharField( max_length=256 )
    slug = AutoSlugField( populate_from='name', unique=True )

    # memberships
    members = models.ManyToManyField( Person, through='Membership' )
    sublists = models.ManyToManyField( 'self', symmetrical=False, blank=True, null=True )

    # state
    STATES = (
        ('un', 'unknown: investigate'),
        ('kn', 'known: not to be migrated'),
        ('of', 'old format: should be migrated'),
        ('f1', 'new format: fine as is'),
    )
    state = models.CharField( max_length=2, choices=STATES, default='un' )

    def owners(self):
        return self.membership_set.filter(role='OWNER')

    def __unicode__(self):
        return self.email


class Membership(models.Model):
    group = models.ForeignKey(Group)
    person = models.ForeignKey(Person)
    role = models.CharField( max_length=64 )

    def __unicode__(self):
        return u'%s in %s' % ( self.person, self.group )

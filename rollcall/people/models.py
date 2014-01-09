import md5

from django.db import models

from autoslug import AutoSlugField



class Person(models.Model):
    name = models.CharField( max_length=256 )
    email = models.CharField( max_length=256, unique=True )
    google_id = models.CharField( max_length=64 )
    slug = AutoSlugField( populate_from='name', unique=True )

    @property
    def avatar_url(self):
        return 'http://gravatar.com/avatar/%s' % md5.new(self.email).hexdigest()

    def manager(self):
        for membership in self.membership_set.filter(role='MEMBER'):
            if membership.group.email.find('gds-reports') == 0:
                first_owner = membership.group.owners()[0]
                return first_owner.person
        return None

    def memberships(self):
        return self.membership_set.all()

    def owns(self):
        return self.membership_set.filter(role='OWNER')

    def __unicode__(self):
        return self.name

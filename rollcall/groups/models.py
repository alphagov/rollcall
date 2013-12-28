from django.db import models

from autoslug import AutoSlugField



class Group(models.Model):
    name = models.CharField( max_length=256 )
    email = models.CharField( max_length=256 )
    description = models.CharField( max_length=256 )
    slug = AutoSlugField( populate_from='name', unique=True )

    def __unicode__(self):
        return self.email

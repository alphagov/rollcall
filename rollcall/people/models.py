from django.db import models

from autoslug import AutoSlugField



class Person(models.Model):
    name = models.CharField( max_length=256 )
    email = models.CharField( max_length=256, unique=True )
    google_id = models.CharField( max_length=64 )
    slug = AutoSlugField( populate_from='name', unique=True )

    def __unicode__(self):
        return self.name

from django.db import models
from datetime import datetime

from catalog2.contact.models import Contact

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Model(models.Model):
    camera_brand = models.ForeignKey(Brand)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s %s" % (self.camera_brand, self.name)


class Catalog(models.Model):
    camera_model = models.ForeignKey(Model)
    who = models.ForeignKey(Contact, default=6)

    date = models.DateTimeField(default=datetime.now)
    is_borrowed = models.BooleanField(default=False)
    given = models.BooleanField(default=False)
    gift = models.BooleanField(default=False)

    WORKING_CHOICES = (
        ('Y', 'yes'),
        ('N', 'no'),
        ('M', 'maybe'),
        ('L', 'maybe not')
    )
    working = models.CharField(max_length=1, choices=WORKING_CHOICES)

    price = models.IntegerField(default=0)
    sn = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=1024, null=True, blank=True)

    @property
    def loaded(self):
        return (self.incamera.filter(loaded=True).all() or [None])[0]

    def __unicode__(self):
        return "%s : %s (%s)" % (self.camera_model, self.sn, self.comment)


class Encyclopedia(models.Model):
    camera_model = models.ForeignKey(Model)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s : %s" % (self.key, self.value)

from django.db import models
from django.db.models import Sum
from datetime import datetime

from catalog2.contact.models import Contact

# Create your models here.
class LensMount(models.Model):
    name = models.CharField(max_length=255)

    @property
    def lenses(self):
        return Catalog.objects.filter(mount=self)


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Model(models.Model):
    lense_brand = models.ForeignKey(Brand)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s %s" % (self.lense_brand, self.name)


class Catalog(models.Model):
    lense_model = models.ForeignKey(Model)
    who = models.ForeignKey(Contact, default=6, related_name='lens')

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

    mount = models.ForeignKey(LensMount)

    def __unicode__(self):
        label = unicode(self.lense_model)
        label += " : %s" % self.sn if self.sn else ''
        label += " (%s)" % self.comment if self.comment else ''
        return label

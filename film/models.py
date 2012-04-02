import uuid
from datetime import datetime

from django.db import models
from catalog2.contact.models import Developer
from catalog2.camera.models import Catalog as CameraCatalog

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Ref(models.Model):
    film_brand = models.ForeignKey(Brand)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s %s" % (self.film_brand, self.name)


class Sensitivity(models.Model):
    iso = models.IntegerField()

    def __unicode__(self):
        return "%s ISO" % self.iso


class Catalog(models.Model):
    film_ref = models.ForeignKey(Ref)
    film_sensitivity = models.ForeignKey(Sensitivity)

    comment = models.CharField(max_length=1024, null=True)
    quantity = models.IntegerField(default=1)
    expiration = models.DateField(null=True, blank=True)
    buy_date = models.DateField(default=datetime.now().date)

    POSES_CHOICES = (
        ('12', '12'),
        ('20', '20'),
        ('24', '24'),
        ('36', '36'),
    )
    poses = models.CharField(max_length=2, choices=POSES_CHOICES)

    COLOR_CHOICES = (
        ('1', 'BW'),
        ('2', 'negative'),
        ('3', 'diapo'),
    )
    color = models.CharField(max_length=1, choices=COLOR_CHOICES)

    FORMAT_CHOICES = (
        ('1', '24x36'),
        ('2', '120'),
        ('3', '220'),
        ('4', '620'),
    )
    format = models.CharField(max_length=1, choices=FORMAT_CHOICES)

    def __unicode__(self):
        return "%s (%s)" % (self.film_ref, self.film_sensitivity)


def get_handle():
    return uuid.uuid1().hex


class Life(models.Model):
    film_catalog = models.ForeignKey(Catalog)
    shoot_sensitivity = models.ForeignKey(Sensitivity, related_name='shoot',
        null=True, blank=True)
    dev_sensitivity = models.ForeignKey(Sensitivity, related_name='dev',
        null=True, blank=True)
    developer = models.ForeignKey(Developer,
        null=True, blank=True)

    handle = models.CharField(max_length=255, default=get_handle)
    insertion = models.DateTimeField(default=None, null=True, blank=True)
    removal = models.DateTimeField(default=None, null=True, blank=True)
    develop = models.DateTimeField(default=None, null=True, blank=True)
    reference = models.CharField(max_length=16, null=True, blank=True)

    def __unicode__(self):
        return "%s [%s/%s]" % (self.film_catalog, self.handle, self.reference)


class InCamera(models.Model):
    film_life = models.ForeignKey(Life)
    camera_catalog = models.ForeignKey(CameraCatalog)

    loaded = models.BooleanField(default=True)
    poses = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s %s" % (
            self.film_life,
            'in' if self.loaded else 'from',
            self.camera_catalog)

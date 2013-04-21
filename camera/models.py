from django.db import models
from django.db.models import Sum
from datetime import datetime

from catalog2.contact.models import Contact
from catalog2.lens.models import LensMount

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Model(models.Model):
    camera_brand = models.ForeignKey(Brand)
    name = models.CharField(max_length=255)
    mount = models.ForeignKey(LensMount, related_name='camera',
        null=True, blank=True)
    fixed_lens = models.BooleanField()

    def __unicode__(self):
        return "%s %s" % (self.camera_brand, self.name)

    @property
    def encyclopedia(self):
        return Encyclopedia.objects.filter(camera_model=self)


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

    STATUS_CHOICE = (
        ('o', 'own'),
        ('g', 'selling'),
        ('s', 'sold'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='o')
    sell_price = models.IntegerField(null=True, blank=True)
    sell_reason = models.CharField(max_length=1024, null=True, blank=True)
    sell_date = models.DateTimeField(null=True, blank=True)

    @property
    def loaded(self):
        return (self.incamera.filter(loaded=True).all() or [None])[0]

    @property
    def num_films(self):
        return self.incamera.count()

    @property
    def gotit(self):
        return self.sell_date is None

    @classmethod
    def total_sum(cls):
        return cls.objects.aggregate(Sum('price'))['price__sum']

    def selling(self, price, comment):
        self.sell_price = price
        self.sell_reason = comment
        self.status = 'g'

    def sold(self):
        self.sell_date = datetime.now()
        self.status = 's'

    def __unicode__(self):
        label = unicode(self.camera_model)
        label += " : %s" % self.sn if self.sn else ''
        label += " (%s)" % self.comment if self.comment else ''
        return label


class Encyclopedia(models.Model):
    camera_model = models.ForeignKey(Model)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s : %s" % (self.key, self.value)

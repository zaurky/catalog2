import uuid
from datetime import datetime, date

from django.db import models
from catalog2.contact.models import Developer
from catalog2.camera.models import Catalog as CameraCatalog
from catalog2.camera.models import Model as CameraModel

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


class Format(models.Model):
    name = models.CharField(max_length=5)
    cameras = models.ManyToManyField(CameraModel,
        related_name='possible_film_format', null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.name


class Catalog(models.Model):
    film_ref = models.ForeignKey(Ref)
    film_sensitivity = models.ForeignKey(Sensitivity)
    film_format = models.ForeignKey(Format)

    comment = models.CharField(max_length=1024, null=True, blank=True)
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
        ('BW', 'BW'),
        ('negative', 'negative'),
        ('diapo', 'diapo'),
    )
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)

    @property
    def remaining(self):
        #TODO incamera can be '', should filter on that too
        return self.lifes.filter(incamera=None).all()

    @property
    def expired(self):
        return self.expiration < date.today()

    def __unicode__(self):
        return "%s (%s %s) [%s]" % (
            self.film_ref, self.film_sensitivity, self.expiration, len(self.remaining) or 'X')

    def save(self, *args, **kargs):
        ret = super(Catalog, self).save(*args, **kargs)
        if self.quantity and not self.lifes.count():
            # this is creation time
            for i in range(0, self.quantity):
                l = Life(film_catalog=self)
                l.save()
        return ret


def get_handle():
    return uuid.uuid1().hex


class DevelopProcess(models.Model):
    temperature = models.IntegerField(default=20)


class DevelopProcessElements(models.Model):
    name = models.CharField(max_length=1024)
    duration = models.IntegerField()
    process = models.ForeignKey(DevelopProcess, related_name='element')


class Life(models.Model):
    film_catalog = models.ForeignKey(Catalog, related_name='lifes')
    shoot_sensitivity = models.ForeignKey(Sensitivity, related_name='shoot',
        null=True, blank=True)
    dev_sensitivity = models.ForeignKey(Sensitivity, related_name='dev',
        null=True, blank=True)
    developer = models.ForeignKey(Developer, null=True, blank=True)
    dev_process = models.ForeignKey(DevelopProcess, null=True, blank=True)

    handle = models.CharField(max_length=32, default=get_handle)
    insertion = models.DateTimeField(default=None, null=True, blank=True)
    removal = models.DateTimeField(default=None, null=True, blank=True)
    develop = models.DateTimeField(default=None, null=True, blank=True)
    reference = models.CharField(max_length=4, null=True, blank=True)
    comment = models.CharField(max_length=1024, null=True, blank=True)

    @classmethod
    def next_reference(cls):
        last_live = Life.objects.filter(reference__isnull=False
                                        ).order_by('-reference')
        if not last_live:
            return "%04d" % 1

        return "%04d" % (int(last_live[0].reference) + 1)

    @property
    def unloaded(self):
        if self.incamera.count():
            incamera = self.incamera.get()
            if not incamera.loaded:
                return incamera

    @property
    def loaded(self):
        if self.incamera.count():
            incamera = self.incamera.get()
            if incamera.loaded:
                return incamera

    @property
    def developed(self):
        return self.unloaded and self.develop is not None

    @property
    def filmsheet(self):
        if self.filmsheet_set.count():
            return self.filmsheet_set.all()[0].media

    def load(self):
        self.insertion = datetime.now()

    def unload(self):
        self.removal = datetime.now()
        self.reference = self.next_reference()

    def devel(self, contact, iso=None):
        self.develop = datetime.now()
        self.developer = contact
        if iso:
            self.dev_sensitivity = iso

    def reinit(self):
        '''should be called when linked by mistake'''
        self.shoot_sensitivity = None
        self.dev_sensitivity = None
        self.developer = None
        self.insertion = None
        self.removal = None
        self.develop = None
        self.reference = None
        self.comment = None
        if self.incamera.count():
            incamera = self.incamera.get()
            incamera.delete()

    @classmethod
    def last_inserted(cls):
        lifes = map(lambda ic:
            ic.film_life, InCamera.objects.filter(loaded=True))
        lifes.sort(lambda a,b: cmp(b.insertion, a.insertion))
        return lifes[0] if lifes else None

    def __unicode__(self):
        return "%s [%s]%s%s" % (self.film_catalog, self.reference,
            " *" if self.incamera.count() else "",
            " (p)" if self.filmsheet else "")

    def __cmp__(self, other):
        return cmp(self.reference, other.reference) and \
            cmp(self, other)


class InCamera(models.Model):
    film_life = models.ForeignKey(Life, related_name='incamera')
    camera_catalog = models.ForeignKey(CameraCatalog, related_name='incamera')

    loaded = models.BooleanField(default=True)
    poses = models.IntegerField(null=True, blank=True)

    def load(self):
        self.loaded = True

    def unload(self, poses):
        self.loaded = False
        self.poses = poses

    def __unicode__(self):
        return unicode(self.film_life) + \
            (' in ' if self.loaded else ' from ') + \
            unicode(self.camera_catalog)

    def __cmp__(self, other):
        return cmp(self.film_life.reference, other.film_life.reference)

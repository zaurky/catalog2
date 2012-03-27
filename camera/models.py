from django.db import models

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
    date = models.DateTimeField()
    is_borrowed = models.BooleanField()
    given = models.BooleanField()
    gift = models.BooleanField()

    WORKING_CHOICES = (
        ('Y', 'yes'),
        ('N', 'no'),
        ('M', 'maybe'),
        ('L', 'maybe not')
    )
    working = models.CharField(max_length=1, choices=WORKING_CHOICES)

    price = models.IntegerField()
    sn = models.CharField(max_length=255)
    comment = models.CharField(max_length=1024)

    def __unicode__(self):
        return "%s : %s (%s)" % (self.camera_model, self.sn, self.comment)

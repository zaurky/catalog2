from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    homemade = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s [%s - %s]" % (self.name, self.town, self.country)

from django.db import models

from catalog2.camera.models import Model as CameraModel
from catalog2.film.models import Life as FilmLife

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % (self.name)


class Media(models.Model):
    tag = models.ManyToManyField(Tag, related_name='media')

    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    @property
    def tags(self):
        return self.tag.all()

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.comment)


class Camera(models.Model):
    camera_model = models.ForeignKey(CameraModel, related_name='camera')
    media = models.ForeignKey(Media)

    def __unicode__(self):
        return "%s <-> %s" % (self.media.name, self.camera_model)


class Exemple(models.Model):
    film_life = models.ForeignKey(FilmLife, related_name='exemple')
    media = models.ForeignKey(Media)

    def __unicode__(self):
        return "%s <-> %s" % (self.media.name, self.film_life.film_catalog)


class FilmSheet(models.Model):
    film_life = models.ForeignKey(FilmLife, related_name='filmsheet_set')
    media = models.ForeignKey(Media)

    def __unicode__(self):
        return "%s <-> %s" % (self.media.name, self.film_life)

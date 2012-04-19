from django.db import models

from catalog2.camera.models import Model as CameraModel
from catalog2.film.models import Life as FilmLife

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Media(models.Model):
    tag = models.ManyToManyField(Tag, related_name='media')

    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    url = models.CharField(max_length=255)


class Camera(models.Model):
    camera_model = models.ForeignKey(CameraModel)
    media = models.ForeignKey(Media)


class Exemple(models.Model):
    film_life = models.ForeignKey(FilmLife)
    media = models.ForeignKey(Media)


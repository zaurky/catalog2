from django.db import models
from catalog2.film.models import Life

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    buy_date = models.DateTimeField(null=True, blank=True)
    opening_date = models.DateTimeField(null=True, blank=True)
    should_be_done_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class ProductToLife(models.Model):
    product = models.ForeignKey(Product)
    film_life = models.ForeignKey(Life)

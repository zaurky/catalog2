from django.db import models
from catalog2.film.models import Life

# Create your models here.


class Product(models.Model):
    film_life = models.ManyToManyField(Life, related_name='products')
    name = models.CharField(max_length=100)
    buy_date = models.DateTimeField(null=True, blank=True)
    opening_date = models.DateTimeField(null=True, blank=True)
    should_be_done_date = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

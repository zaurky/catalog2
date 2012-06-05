#!/usr/bin/python

from film.models import *

for life in Life.objects.filter(reference='', incamera=None):
    print life
    life.clean()
    life.save()

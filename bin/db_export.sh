#!/bin/sh

for model in camera.brand camera.model camera.catalog camera.encyclopedia film.brand film.ref film.sensitivity film.catalog film.life film.incamera contact.contact contact.developer develop.product develop.producttolife; do
    app=`echo $model | sed -e 's/\..*//'`
    app_table=`echo $model | sed -e 's/.*\.//'`
    python manage.py dumpdata $model > $app/fixtures/$app_table.json
done

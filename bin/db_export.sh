#!/bin/sh

. conf/catalog.sh
MODELS=`echo $TABLES | sed -e 's/#/./g'`

for model in $MODELS; do
    app=`echo $model | sed -e 's/\..*//'`
    app_table=`echo $model | sed -e 's/.*\.//'`
    python manage.py dumpdata $model > $app/fixtures/$app_table.json
done

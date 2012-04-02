#!/bin/sh

TABLES='develop_product contact_contact contact_developer film_sensitivity film_brand camera_brand camera_model film_ref film_catalog camera_catalog camera_encyclopedia film_life film_incamera develop_producttolife'

for T in $TABLES; do
    sqlite3 db/catalog2.sqlite3 "DROP TABLE $T;"
done

python manage.py syncdb

for T in $TABLES; do
    T=`echo $T | sed -e 's/.*_//'`
    echo $T
    python manage.py loaddata $T
done


#!/bin/sh

. conf/catalog.sh

for T in $TABLES; do
    sqlite3 db/catalog2.sqlite3 "DROP TABLE $T;"
done

python manage.py syncdb

for T in $TABLES; do
    T=`echo $T | sed -e 's/.*_//'`
    echo $T
    python manage.py loaddata $T
done


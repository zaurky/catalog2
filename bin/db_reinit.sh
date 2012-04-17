#!/bin/sh

. conf/catalog.sh

for TABLE in $TABLES; do
    sqlite3 db/catalog2.sqlite3 "DROP TABLE $TABLE;"
done

python manage.py syncdb

for TABLE in $TABLES; do
    TABLE=`echo $TABLE | sed -e 's/.*#//'`
    echo $TABLE
    python manage.py loaddata $TABLE
done


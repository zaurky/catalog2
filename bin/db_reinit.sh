#!/bin/sh

. conf/catalog.sh

for TABLE in $TABLES; do
    TABLE=`echo $TABLE | sed -e 's/#/_/g'`
    echo "DROP TABLE $TABLE"
    sqlite3 db/catalog2.sqlite3 "DROP TABLE $TABLE;"
done

python manage.py syncdb

for TABLE1 in $TABLES; do
    TABLE=`echo $TABLE1 | sed -e 's/.*#//'`
    SQLTABLE=`echo $TABLE1 | sed -e 's/#/_/g'`
    echo $TABLE
    if [ `sqlite3 db/catalog2.sqlite3 "SELECT COUNT(*) FROM $SQLTABLE;"` -ne 0 ]; then
	echo 'delete from'
        sqlite3 db/catalog2.sqlite3 "DELETE FROM $SQLTABLE;"
    fi
    python manage.py loaddata $TABLE
done


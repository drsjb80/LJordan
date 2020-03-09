
# HPotter
Simple Python JSON server for [HPotter](https://github.com/drsjb80/HPotter)

<!-- [![Build Status](https://travis-ci.org/drsjb80/HPotter.svg?branch=master)](https://travis-ci.org/drsjb80/HPotter) -->

## Running and developing

INSTALL necessary packages:

    pip install -r requirements.txt
    or
    pip3 install -r requirements.txt

CONFIGURE the location of the database

This package assumes:
* HPotter stores data in a sqlite database located at .../HPotter/main.db
* The HPotter and LJordan modules are in the same directory
```
    .../
        HPotter/
            main.db
        LJordan/
```

To change the path to main.db, update the `dbPath` in env.py.

RUN the SQL to JSON server

    python3 -m jsonserver

Once jsonserver is running, you can request json dumps of tables in tables.py using

    curl localhost:8000/<tableName>
    for example
    curl localhost:8000/connections

## NOT YET IMPLEMENTED
Once the jsonserver is running, you can see the current data by loading the
ajax.html file that is in the directory above into your web browser.

To see the current contents of the database, do:
    sqlite3 -list main.db .dump

The JSON API is easy to query. To get all the data, go to localhost:8080:

    curl localhost:8080

If you're interested in a particular table, reference that:

    curl localhost:8080/sh

If you want to use JSONP, pass a callback:

    curl localhost:8080/?callback=jQuery

To get JSON in the form to use with jTables, do:

    curl localhost:8080/?handd=true

## Thanks
This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>.

Configuring config.ini Parameters
=================================

Introduction
------------

The config.ini file contains the parameters to connect to the database and path of csv files to be
loaded.

Editing config.ini
------------------

Example of config.ini

.. code-block :: python

    [__main__]
    database = name_database
    user = admin
    passwd = 12345
    csv = ~/invoice.csv
          ~/invoice_lines.csv

The parameters is in each line with its value. In example, the name of database is `name_database`.
the database user is `admin` and its password `12345`.

The csv fiels is listed by order. By example, the csv with invoice must be loaded before
that csv with invoice lines, since, it is preferable to fill a many2one field than a one2many
field. From invoice_lines must be filled the invoice_id field, referring to the invoice to which it
belongs.

Parameters Required
~~~~~~~~~~~~~~~~~~~

#. **database**: Name of the database to connect.
#. **user**: Username to use for the connection.
#. **passwd**: Password to use fot the connection.

Parameters Optional
~~~~~~~~~~~~~~~~~~~

#. **csv**: CSV File to load. By default is empty. 
#. **server**: Host where the database engine is listening on. By default is **'localhost'**.
#. **port**: Port where the database engine is listening on. By default is **8069**.
#. **timeout**: Time out for connection. By default is **4000**.


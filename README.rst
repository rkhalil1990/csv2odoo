csv2odoo
========

csv2odoo is a webservice that handles uploading CSV data to your Odoo database.

Use of the csv2odoo tool consists of three basic steps: 

#. Creating CSV file with the data to be loaded. 
#. Edit the config.ini file: 
    #) Configuring the connection parameter to the database 
    #) Add the path to the csv files to be uploaded. 
#. Run the script.

---

csv2odoo es un webservice que se encarga de subir datos desde un csv a tu base de datos de Odoo.

El uso de la herramienta csv2odoo consiste en tres pasos básicos:

#. Crear archivos csv con la data a ser cargada
#. Editar el archivo config.ini:
   #) Configurar los parámetro de conexión a la base de datos.
   #) Agregar la ruta correspondiente a los archivos csv a ser subidos.
#. Correr el script

WARNING!
--------

For best practices is recommended fill one2many fields from the model to which it relates. 
For example, if we add lines to an invoice, instead of creating the lines and then assign them to
the invoice, we can create the invoice first and then, on the lines assign a invoice_id. 

This is because, if we want to run our script and we changed the value of a one2many field in a 
csv, and we have assigned the value empty, the above values are not erased.

---

Para mejores prácticas es recomendable llenar los campos one2many desde el modelo al cual se
relaciona. Por ejemplo, si debemos agregar líneas a una factura, en lugar de crear las líneas y
luego asignarlas a la factura, podremos crear la factura primero, y luego, en las líneas asignarle
un invoice_id.

Esto se debe a que, si quisieramos correr nuestro script y hemos cambiado el valor de un
campo one2many en algún csv, y hemos asignado vacio al valor, los valores anteriores
no se borrarán.


.. TO DO
.. -----
.. 
.. #. Cuando el csv tiene varios campos y en la fila de los datos no se completan
..    los delimitadores (,) ocurre un error.
.. 
.. Errores
.. -------
.. 
.. [-1, {}, "Line 1 : 'bool' object is not iterable", '']
.. 
.. Ocurre cuando se hace referencia a un campo one2many en el csv,
.. en el cual, dejas el valor en blanco, y en la base de datos no existe
.. ningun registro hacia el modelo al que hace relacion el campo.
.. 
.. Hace falta completar las ',' en el csv

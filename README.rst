Correr el ejemplo
-----------------

- Instalar modulos: **account_accountant** y **hr**.
- Configurar: nombre de BD, usuario y password en archivo config.ini (Dejar variable csv como está).
- Correr el script: **python csvopen.py.**

TO DO
-----

#. Cuando el csv tiene varios campos y en la fila de los datos no se completan
   los delimitadores (,) ocurre un error.

Errores
-------

[-1, {}, "Line 1 : 'bool' object is not iterable", '']

Ocurre cuando se hace referencia a un campo one2many en el csv,
en el cual, dejas el valor en blanco, y en la base de datos no existe
ningun registro hacia el modelo al que hace relacion el campo.

Hace falta completar las ',' en el csv

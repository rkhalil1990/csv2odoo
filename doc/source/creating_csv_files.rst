Creating CSV Files
==================

Introduction
------------

The CSV files contains data to be loaded in database.

The CSV files have three parts:

#. **Field name**: The name of field in database.
#. **Metadata**: Depending of field type (char, selection, one2many, many2one, etc) must be filled
   the metadata. This information tells to csv2odoo how the value should be loaded.
#. **Field Value**: The data to be loaded.

Fields required
---------------

`id` and `model` are fields required in all csv.
By example, one basic csv is `hr.employee.category`.

.. code-block :: xml

    id,model,name
    str,str,str
    hr_employee_category_001,hr.employee.category,category1
    hr_employee_category_002,hr.employee.category,category2

#. **id** represents the xml id of registry.
#. **model** is the Odoo model.

Metadata for each field type.
-----------------------------

Metadata **str**
~~~~~~~~~~~~~~~~

**str** metadata is used when the value is write as such in the database.

this applies to the fields:

'boolean', 'integer', 'date', 'datetime', 'char', 'binary', 'float', 'text', 'selection'
and 'reference'.

Example:

- **char**: (name) -> Dennis Ritchie 
- **date**: (birthday) -> 1941-09-09
- **boolean**: (active) -> 1 for True and 0 for False.
- **integer**: (age) -> 70
- **datetime**: (last_login) -> 2011-10-25 14:04:34
- **float**: (height) -> 1.70
- **text**: (description) -> Was an American computer scientist. He created the C programming language.
- **selection**: (gender) -> male or female
- **binary**: (image) -> [Binary here]
  
.. code-block :: xml

    id,model,name,birthday,active,age,last_login,height,description,gender,image
    str,str,str,str,str,str,str,str,str,str,str
    person_001,person.person,Dennis Ritchie,1941-09-09,0,70,2011-10-25 14:04:34,1.70,"Was an American computer scientist. He created the C programming language.",male,"QfjqfZeO8L+0Z8BuJaAGWlgIIn8xB1HYLacH5roP0qsc...."


Metadata **ref**
~~~~~~~~~~~~~~~~

**ref** metadata is used for relational field. After writing the name of field should be written ":id"

this applies to the fields:

'many2one', 'many2many' and 'one2many'

Example:

- **many2one**:  (company_id) -> base.main_company 
- **many2many**: (category_ids) -> hr_employee_category_001;hr_employee_category_002

.. code-block :: xml

    id,model,name,company_id:id,category_ids:id
    str,str,str,ref,ref
    hr_employee_001,hr.employee,José Toro,base.main_company,hr_employee_category_001;hr_employee_category_002

.. note ::

    For one2many fields is equal to many2one or many2many. But, not recommended for use

Metadata **search;field**
~~~~~~~~~~~~~~~~~~~~~~~~~

**search;field** metadata is used for relational field. After writing the name of field should be
written ":id". When writing metadata, search, field, field should refer to the name of the field
where you will search.

this applies to the fields:

'many2one', 'many2many' and 'one2many'

Example:

- **many2one**:  (company_id) ->  department1
- **many2one**:  (journal_id) ->  00001
- **many2many**: (category_ids) -> category1;category2

.. code-block :: xml

    id,model,name,department_id:id,category_ids:id,journal_id:id
    str,str,str,search;name,search;name,search;code
    hr_employee_001,hr.employee,José Toro,department1,category1;category2,00001

.. note ::

    For one2many fields is equal to many2one or many2many. But, not recommended for use


.. elif tipo in ('function', 'related', 'property'):

Examples
--------

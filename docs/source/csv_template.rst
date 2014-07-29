CSV Templates
=============

Order in which should be executed the csv in the config.ini.

.. code-block :: python

    csv = csv_templates/purchase_order/purchase_order_required.csv
          csv_templates/purchase_order/purchase_order.csv
          csv_templates/purchase_order/purchase_order_line.csv
          csv_templates/account_move_line/account_move.csv
          csv_templates/account_move_line/account_move_line.csv

purchase_order
--------------

Because the model has many fields, two csv is created
(purchase_order_required.csv and purchase_order.csv),
purchase_order_required.csv have required fields and purchase_order.csv have
optional fields.

purchase_order_required.csv
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block :: xml

    id,model,partner_id:id,location_id:id,pricelist_id:id
    str,str,search;name,search;name,search;name
    purchase_order_001,purchase.order,Supplier1,Stock,Default Purchase Pricelist
    purchase_order_002,purchase.order,Supplier2,Stock,Default Purchase Pricelist

purchase_order.csv
~~~~~~~~~~~~~~~~~~

.. code-block :: xml

    id,model,partner_ref,invoice_method,invoiced,payment_term_id:id,minimum_planned_date,shipped,validator:id,date_approve,fiscal_position:id,origin
    str,str,str,str,str,search;name,str,str,search;name,str,search;name,str
    purchase_order_001,purchase.order,RefPartner1,order,0,30 Net Days,2013-07-25,0,Administrator,2014-01-28,Normal Taxes,Doc1
    purchase_order_002,purchase.order,RefPartner2,order,1,15 Days,2011-07-23,1,Administrator,2014-01-28,Tax Exempt,Doc2

purchase_order_line.csv
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block :: xml

    id,model,order_id:id,product_id:id,name,date_planned,product_qty,price_unit,taxes_id
    str,str,ref,search;name,str,str,str,str,search;name
    purchase_order_line_001,purchase.order.line,purchase_order_001,Service,Services,2013-01-01,4,567.98,
    purchase_order_line_002,purchase.order.line,purchase_order_001,Service,Services 2,2013-01-01,1,789.67,
    purchase_order_line_003,purchase.order.line,purchase_order_001,Service,Services 3,2013-01-01,10,87.36,

account_move
------------

account_move.csv
~~~~~~~~~~~~~~~~

.. code-block :: xml

    id,model,journal_id:id,period_id:id,date,ref
    str,str,search;name,search;code,str,str
    account_move_001,account.move,Cash,07/2014,2014-07-29,

account_move_line.csv
~~~~~~~~~~~~~~~~~~~~~

.. code-block :: xml

    id,model,name,date,account_id:id,ref,partner_id:id,move_id:id,debit,credit,journal_id:id,period_id:id,account_tax_id
    str,str,str,str,search;code,str,search;name,ref,str,str,search;name,search;name,search;code
    account_move_line_001,account.move.line,AML_001,2014-01-07,110200,,,account_move_001,300.00,0.0,Cash,01/2014,
    account_move_line_002,account.move.line,AML_002,2014-01-07,110200,,,account_move_001,0.0,100.0,Cash,01/2014,
    account_move_line_003,account.move.line,AML_003,2014-01-07,110200,,,account_move_001,0.0,200.0,Cash,01/2014,

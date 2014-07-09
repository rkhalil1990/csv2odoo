# -*- coding: utf-8 -*-
from configglue import schema
from configglue.glue import configglue
import oerplib
import libxml2
import csv
import pdb

variables = ['server', 'port', 'timeout', 'database', 'user', 'passwd', 'csv']

class MySchema(schema.Schema):

    server = schema.StringOption(
        default='localhost',
        help='Host where the database engine is listening on')
    port = schema.IntOption(
        default=8069,
        help='Port where the database engine is listening on')
    timeout = schema.IntOption(
        default=4000,
        help='Time out for connection')
    database = schema.StringOption(
        fatal=True,
        help='Name of the database to connect to')
    user = schema.StringOption(
        help='Username to use for the connection')
    passwd = schema.StringOption(
        help='Password to use fot the connection')
    csv = schema.ListOption(
        item = schema.StringOption(),
        help='CSV File to read')


def print_values(config, opts):

    values = config.values('__main__')

    for opt in variables:
        option = config.schema.section('__main__').option(opt)
        value = values.get(opt)
        if value != option.default:
            print "%s option has been configured with value: %s" % (opt,
                value)
        else:
            print "%s option has default value: %s" % (opt, option.default)

def read_csv(csv_files, oerp):
    for csv_name in csv_files: 
        lines = csv.reader(open(csv_name))
        field_names = lines.next()
        field_names.remove('model') # field name model deleted
        fields_type = lines.next()
        fields_type.pop(1) # type model deleted

        ir_model_data_obj = oerp.get('ir.model.data')

        datas = []

        for line in lines:
            model_str = line.pop(1)
            model_obj = oerp.get(model_str)

            pdb.set_trace()
            datas.append(line)

        for field in field_names:
            field = field.split(':')[0]
            if field != 'id' and field != 'model':
                tipo = model_obj.__dict__['_browse_class'].__dict__['__osv__'].get('columns').get(field).__dict__.get('type')
                
                if tipo == 'many2one':
                    relation = model_obj.__dict__['_browse_class'].__dict__['__osv__'].get('columns').get(field).__dict__.get('relation')
                    print 'campo: ' + field + ', tipo: ' + tipo + ', relation: ' + relation
                else:
                    print 'campo: ' + field + ', tipo: ' + tipo

        print model_obj.import_data(field_names, datas, mode='init')

def main(config, opts):
    #print_values(config, opts)
    #exit()
    values = config.values('__main__')

    #Extracting parameters in variables
    for var in variables:
        exec("%s = values.get('%s')" % (var,var))

    oerp = oerplib.OERP(server=server, port=port, timeout=timeout)
    admin_brw = oerp.login(user=user, passwd=passwd , database=database)

    read_csv(csv, oerp) 

if __name__ == '__main__':

    glue = configglue(MySchema, ['config.ini'])

    main(glue.schema_parser, glue.options)

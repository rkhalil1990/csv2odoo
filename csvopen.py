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

def get_field_type(field, model_obj):
    return model_obj.__dict__['_browse_class'].__dict__['__osv__'].get('columns').get(field).__dict__.get('type')

def get_xml_id(field, tipo, csv_type, value, model_obj, ir_model_data_obj, oerp):

    xml_id_str = False
    if tipo == 'many2one':
        #pdb.set_trace()
        csv_type = csv_type.split(';')
        if csv_type[0] == 'ref':
            return value
        elif csv_type[0] == 'search':
            #pdb.set_trace()
            field_search = csv_type[1]
            relation_model_str = model_obj.__dict__['_browse_class'].__dict__['__osv__'].get('columns').get(field).__dict__.get('relation')
            print 'campo: ' + field + ', tipo: ' + tipo + ', relation: ' + relation_model_str
            relation_model_obj = oerp.get(relation_model_str)
            field_id = relation_model_obj.search([(field_search,'=',value)])[0]

            #_get_xml_id openerp/osv/orm.py +1125
            xml_id = ir_model_data_obj.search([('model', '=', relation_model_str), ('res_id',
                '=', field_id)])
            if len(xml_id):
                d = ir_model_data_obj.read(xml_id, ['name', 'module'])[0]
                if d['module']:
                    xml_id_str = '%s.%s' % (d['module'], d['name'])
                else:
                    xml_id_str = d['name']

            else:
                postfix = 0
                while True:
                    n = relation_model_str+'_'+str(field_id) + (postfix and ('_'+str(postfix)) or '' )
                    if not ir_model_data_obj.search([('name', '=', n)]):
                        break
                    postfix += 1
                ir_model_data_obj.create({
                    'name': n,
                    'model': relation_model_str,
                    'res_id': field_id,
                    'module': '__export__',
                })
                xml_id_str = '__export__.'+n
            #_get_xml_id END

            return xml_id_str
    elif tipo == 'char':
        return value
    elif tipo == 'date':
        #Revisar correcta sintaxis del date
        print value


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

            datas.append(line)

        for data in datas:
            for i in xrange(0, len(field_names)):
                #Preguntar aqui de que modo viene la informacion para poder buscar el xml_id que
                #le corresponde
                if data[i]:
                    field = field_names[i]
                    field = field.split(':')[0]
                    if field not in ('id', 'model'):
                        tipo = get_field_type(field, model_obj)
                       
                        xml_id = get_xml_id(field, tipo, fields_type[i], data[i], model_obj,
                                ir_model_data_obj, oerp)
                        data[i] = xml_id


        #pdb.set_trace()
        print datas
        print model_obj.import_data(field_names, datas, mode='init', current_module='__export__')

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

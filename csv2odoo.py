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
        fatal=True,
        help='Username to use for the connection')
    passwd = schema.StringOption(
        fatal=True,
        help='Password to use fot the connection')
    csv = schema.ListOption(
        item=schema.StringOption(),
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
    return model_obj.__dict__['_browse_class'].\
        __dict__['__osv__'].get('columns').get(field).\
        __dict__.get('type')


def _get_xml_id(field_id, relation_model_str, ir_model_data_obj):
    """
    Returns xml id of object to get
    @param field_id: id of the object to which you want to find the xml id
    @param relation_model_str: model of the object to which you want to find the xml id
    @param ir_model_data_obj: object of ids xml table
    """
    #_get_xml_id openerp/osv/orm.py +1125
    xml_id = ir_model_data_obj.search(
        [('model', '=', relation_model_str), ('res_id',
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
            n = relation_model_str + '_' + \
                str(field_id) + (postfix and ('_' + str(postfix)) or '')
            if not ir_model_data_obj.search([('name', '=', n)]):
                break
            postfix += 1
        ir_model_data_obj.create({
            'name': n,
            'model': relation_model_str,
            'res_id': field_id,
            'module': '__export__',
        })
        xml_id_str = '__export__.' + n
    return xml_id_str


def error_value_not_found(field_search, value):
    raise Exception(
        ('Field "%s": An associated value was not found, Value "%s"') %
        (field_search, value))


def transform_csv_info(field, tipo, csv_type, value, model_obj, ir_model_data_obj, oerp):
    """
    Transform the information received from the csv, and then find the xml id calling _get_xml_id
    """

    if tipo in ('boolean', 'integer', 'date', 'datetime', 'time'):
        # Revisar correcta sintaxis
        return value
    elif tipo in ('char', 'binary', 'float', 'text', 'selection', 'reference'):
        #TO DO
        return value
    elif tipo in ('many2one', 'many2many', 'one2many'):
        csv_type = csv_type.split(';')
        if csv_type[0] == 'ref':
            return value
        elif csv_type[0] == 'search':
            field_search = csv_type[1]
            relation_model_str = model_obj.__dict__['_browse_class'].\
                __dict__['__osv__'].get('columns').get(
                    field).__dict__.get('relation')
            relation_model_obj = oerp.get(relation_model_str)
            if tipo in ('many2one'):
                field_id = relation_model_obj.search(
                    [(field_search, '=', value)])
                if field_id:
                    field_id = field_id[0]
                else:
                    error_value_not_found(field_search, value)
                xml_id_str = _get_xml_id(
                    field_id, relation_model_str, ir_model_data_obj)
                return xml_id_str
            elif tipo in ('many2many', 'one2many'):
                values = value.split(';')
                xml_id_str = ''
                for value in values:
                    field_id = relation_model_obj.search(
                        [(field_search, '=', value)])
                    if field_id:
                        field_id = field_id[0]
                    else:
                        error_value_not_found(field_search, value)
                    xml_str = _get_xml_id(
                        field_id, relation_model_str, ir_model_data_obj)
                    xml_id_str = xml_id_str + xml_str + ','
                return xml_id_str[:-1]
    elif tipo in ('function', 'related', 'property'):
        #TO DO
        return value


def read_csv(csv_files, oerp):

    for csv_name in csv_files:
        print csv_name
        lines = csv.reader(open(csv_name))
        field_names = lines.next()
        field_names.remove('model')  # field name model deleted
        fields_type = lines.next()
        fields_type.pop(1)  # type model deleted

        ir_model_data_obj = oerp.get('ir.model.data')

        datas = []

        for line in lines:
            model_str = line.pop(1)
            model_obj = oerp.get(model_str)

            datas.append(line)
        for data in datas:
            fd = field_names[:] #Copy of field_names
            dt = data[:] #Copy of data file
            aux = 0 #when a one2many field is removed, the dt array
                    #should be assigned subtracting this aux to 'i' index
            for i in range(0, len(field_names)):

                #extracting real field name
                field = field_names[i]
                field = field.split(':')[0]

                # id is not considering because it's xml id
                if field not in ('id'):
                    tipo = get_field_type(field, model_obj)
                else:
                    continue

                if len(data) <= i:
                    #when a one2many field is empty. Must be removed from
                    #the list of fields to consider when will import the data.
                    if tipo == 'one2many':
                        fd.remove(field_names[i])
                    continue

                if data[i]:
                    #If information is not null, it's search xml id
                    xml_id = transform_csv_info(
                        field, tipo, fields_type[i], data[i], model_obj,
                        ir_model_data_obj, oerp)
                    data[i] = xml_id
                    dt[i - aux] = xml_id
                else:
                    #when a one2many field is empty. Must be removed from
                    #the list of fields to consider when will import the data.
                    if tipo == 'one2many':
                        fd.remove(field_names[i])
                        dt.pop(i - aux)
                        aux += 1

            result, rows, warning_msg, dummy = model_obj.import_data(
                fd, [dt], mode='init', current_module='__export__')

            if result < 0:
                pdb.set_trace()
                # Report failed import and abort module install
                raise Exception(
                    ('Module loading %s failed: file %s could not be processed:\n %s') %
                    ('', csv_name, warning_msg))
            else:
                print data
                print "It's OK\n"


def main(config, opts):
    #print_values(config, opts)
    # exit()
    values = config.values('__main__')

    # Extracting parameters in variables
    for var in variables:
        exec("%s = values.get('%s')" % (var, var))

    print "***Connecting to server %s:%s..\n." % (server,port)
    oerp = oerplib.OERP(server=server, port=port, timeout=timeout)
    print "***Connection to the server %s:%s was successful.\n" % (server,port)

    print "***Acceding to the database '%s' with user.\n" % (database)
    admin_brw = oerp.login(user=user, passwd=passwd, database=database)
    print "***Access to the instance was successful.\n"

    read_csv(csv, oerp)

if __name__ == '__main__':

    glue = configglue(MySchema, ['config.ini'])

    main(glue.schema_parser, glue.options)

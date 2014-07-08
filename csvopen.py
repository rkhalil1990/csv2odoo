# -*- coding: utf-8 -*-
from configglue import schema
from configglue.glue import configglue
import oerplib
import pdb

variables = ['server', 'port', 'timeout', 'database', 'user', 'passwd']

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

def main(config, opts):
    #print_values(config, opts)

    values = config.values('__main__')

    #Extracting parameters in variables
    for var in variables:
        exec("%s = values.get('%s')" % (var,var))

    oerp = oerplib.OERP(server=server, port=port, timeout=timeout)
    admin_brw = oerp.login(user=user, passwd=passwd , database=database)

if __name__ == '__main__':

    glue = configglue(MySchema, ['config.ini'])

    main(glue.schema_parser, glue.options)

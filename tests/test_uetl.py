import uetl
import pandas as pd

def test_init():
    DWO = uetl.DataWarehouse(name='My DataWarehouse',
                           dbms='postgres',
                           host='192.168.1.0',
                           port='5432',
                           base='dbname',
                           user='foo',
                           pswd='bar')

    assert DWO.name == 'My DataWarehouse'

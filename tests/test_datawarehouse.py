import datawarehouse as dw
import pandas as pd

def test_init():
    DWO = dw.DataWarehouse(name='My DataWarehouse',
                           dbms='postgres',
                           host='192.168.1.0',
                           port='5432',
                           base='dbname',
                           user='foo',
                           pswd='bar')

    assert DWO.name == 'My DataWarehouse'

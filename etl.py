import datawarehouse as dw
import pandas as pd

DWO = dw.DataWarehouse(name='My DataWarehouse',
                       dbms='postgres',
                       host='192.168.2.160',
                       port='5432',
                       base='dwbra',
                       user='dwbra-user',
                       pswd='Hc9iQoOs4xX7mxWeYYzzhA')


# Test dw db connection
if DWO.test_conn():
    print('Data Warehouse DB connection succeed!')
else:
    print('ERROR: Data Warehouse DB failed!')
    exit(-1)

# Query the DW
df = DWO.query("SELECT * FROM DIM_DATE")
print(df.head())

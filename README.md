uETL
====

Minimalist python ETL library.

## Instalation

```python
pip install uetl
```

## Usage

```python
import uetl
import pandas as pd

DWO = uetl.DataWarehouse(name='My DataWarehouse',
                       dbms='postgres',
                       host='192.168.1.1',
                       port='5432',
                       base='db-name',
                       user='foo',
                       pswd='bar')


# Test dw db connection
if DWO.test_conn():
    print('Data Warehouse DB connection succeed!')
else:
    print('ERROR: Data Warehouse DB failed!')
    exit(-1)

# Query the DW
df = DWO.query("SELECT * FROM DIM_DATE")
print(df.head())
```

## Contributing

To install this package allong with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
pip install -e .[dev]
```

Also, it is necessary to install local libraries:

```bash
$ sudo apt-get install libpq-dev
```

## Issues

If you have any problems with or questions about this image, please contact me through a [GitHub issue](https://github.com/andrespp/uetl/issues).

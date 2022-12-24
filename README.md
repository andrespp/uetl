uETL
====

Minimalist python ETL library.

## Instalation

```python
pip install uetl
```

## Usage

### DataWarehouse object

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

### DataSrc object

#### MS SQL Source Object

```python
import uetl
import pandas as pd

host = '192.168.1.1'
port = 49159
base = 'dbname'
user = 'username'
pswd = 'password'

## 1st example - Using 'with' statement

# Create Engine, perform query and dispose engine
with uetl.MssqlSrc('testdb', host, port, base, user, pswd) as SRC:
    print(
        pd.read_sql('select @@version', SRC.engine)
    )

## 2nd example - Create and dispose sqlalchemy engine
db = uetl.MssqlSrc('testdb', host, port, base, user, pswd)
db.create_engine()
print(
    pd.read_sql('select @@version', db.engine)
)
db.dispose()

## 3rd example - Use MssqlSrc.query()
db = uetl.MssqlSrc('testdb', host, port, base, user, pswd)
print(
    db.query('select @@version')
)
```

#### Firebird Source Object

```python
import uetl
import pandas as pd

host = '192.168.1.1'
port = 3050
base = '/path/to/database.fdb'
user = 'sysdba'
pswd = 'masterkey'
chst = 'latin1'

## 1st example - Using 'with' statement
with uetl.FirebirdSrc('testdb', host, port, base, user, pswd) as SRC:
    print(
        pd.read_sql('SELECT * from rdb$database;', SRC.engine)
    )

## 2nd example - Create and dispose sqlalchemy engine
db = uetl.FirebirdSrc('testdb', host, port, base, user, pswd)
db.create_engine()
print(
    pd.read_sql('SELECT * from rdb$database;', db.engine)
)

## 3rd example - Use MssqlSrc.query()
db = uetl.FirebirdSrc('testdb', host, port, base, user, pswd)
print(
    db.query('SELECT * from rdb$database;')
)
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

[MSSql ODBC Driver](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16)

## Issues

If you have any problems with or questions about this image, please contact me through a [GitHub issue](https://github.com/andrespp/uetl/issues).

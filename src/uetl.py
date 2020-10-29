"""utel.py
"""
import pandas as pd
import pandas.io.sql as sqlio
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DataWarehouse():
    """DataWarehouse class
    """

    def __init__(self, name, dbms, host, port, base, user, pswd):
        # Define class attributes
        self.name = name
        self.dbms = dbms
        self.host = host
        self.port = port
        self.base = base
        self.user = user
        self.pswd = pswd

    def postgres_conn(self, host, port, dbname, user, pwd, timeout=3):
        """Connects to PostgreSQL database

        Parameters
        ----------
            host : str
                server name or ip address
            port : int
                server port
            dbname : srt
                database name
            user : srt
                database user
            pwd : srt
                database user's password
            timeout : integer
                connection timeout (defaults to 3 seconds)

        Returns
        -------
            conn :
            Database connection or -1 on error
        """
        conn = \
            psycopg2.connect(host=host,
                             port=port,
                             database=dbname,
                             user=user,
                             password=pwd,
                             connect_timeout=timeout)
        return conn

    def get_conn(self):
        """Connects to the Data Warehouse Database

        Returns
        -------
            conn :
            Database connection or -1 on error
        """
        return self.postgres_conn(self.host, self.port, self.base,
                                  self.user, self.pswd)

    def test_conn(self):
        """Checks if Data Warehouse's DBMS is reachable and DW's database
        exists. If DW DB does not exist, try to create it.

        Returns
        -------
            status : boolean
                True if database is reachable, False otherwise
        """
        conn = self.get_conn()

        if conn == -1: # DW DB Unreachable
            # Try to create DW DB
            if self.create_database(): # DW DB created!
                print('Data Warehouse Database does not exist, creating... ' +
                      'Success!')
                return True
            else:
                # Give up
                return False

        else:
            conn.close()
            return True

    def create_database(self):
        """Creates Data Warehouse's Database

        Returns
        -------
            status : boolean
                True if database was created successfuly, and False otherwise
        """
        # Connect to 'postgres' database in order to be able to create new db
        conn = self.postgres_conn(self.host, self.port, 'postgres',
                                  self.user, self.pswd)
        if conn == -1:
            # DBMS Unreachable!
            return False

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()
        cur.execute("CREATE DATABASE {}  ;".format(self.base))

        conn.close()

        return True

    def check_table(self, table_name):
        """Check if Data Warehouse's table exists.

        Warning
        -------
            Table names are case sensitive!

        Parameters
        ----------
            table_name : srt

        Returns
        -------
            status : boolean
                True if table exist, or False otherwise
        """
        conn = self.get_conn()
        if conn == -1: # DBMS Unreachable!
            return False
        else:
            cur = conn.cursor()
            cur.execute("""
              select exists(
                        select *
                        from information_schema.tables
                        where table_name=%s
                       )""", (table_name,)
            )
            status = cur.fetchone()[0]
            conn.close()
        return status

    def create_tables(self, tables, verbose=False):
        """Creates Data Warehouse's Tables, if it doesn't exist.

        Warning
        -------
            Table names are case sensitive!

        Parameters
        ----------
            tables : dict
                Dictionary containing table_name:sql pairs. Ex.:
                 dict(dim_date='CREATE TABLE dim_data(DATE_SK DOUBLE PRECISION)

            verbose : boolean

        Returns
        -------
            status : boolean
                True if tables already exists or were created successfuly,
              and False otherwise
        """
        for table in tables.keys():

            if not self.check_table(table): # table doesn't exist

                if(verbose):
                    print('Table {} does not exist! Creating... '.format(table),
                      end='')

                conn = self.get_conn()
                if conn == -1: # DBMS Unreachable!
                    print('ERROR: Fail creating tables!')
                    return False
                else:
                    cur = conn.cursor()
                    cur.execute(tables[table])
                    conn.commit()
                    if not self.check_table(table): # Fail to create table
                        print('ERROR: Fail creating tables!')
                        return False
                    if(verbose): print('Success!')
                    conn.close()

        return True

    def truncate(self, table_name, verbose=False):
        """Truncate Table

        Parameters
        ----------
            table_name : str
                Table to be truncated

            verbose : boolean

        Returns
        -------
            status : boolean
                True on success, False otherwise
        """
        if(verbose):
            print('{}: '.format(table_name), end='', flush=True)

        conn = self.get_conn()

        if conn == -1:
            print("ERROR: query(): Unable to connect to the database.")
            return False
        else:
            cur = conn.cursor()
            cur.execute('TRUNCATE {}'.format(table_name))
            conn.commit()
            conn.close()
            if(verbose): print('table truncated.')
            return True

    def write(self, table_name, df, verbose=False, chunksize=None):
        """Write dataframe to table. Dataframe's Index will be used as a column
        named 'table_name'_sk

        Parameters
        ----------
        table_name : str
            Table to be written

        df | Pandas DataFrame
            Data to be loaded

        verbose : boolean

        chunksize : int, optional
            Specify the number of rows in each batch to be written at a time.
            By default, all rows will be written at once.

        Returns
        -------
            status : boolean
                True on success, False otherwise
        """
        if(verbose):
            print('{}: '.format(table_name), end='', flush=True)

        ## psycopg2
        eng_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            self.user, self.pswd, self.host, self.port, self.base)
        engine = create_engine(eng_str)
        conn = self.get_conn()

        if conn == -1:
            print("ERROR: query(): Unable to connect to the database.")
            return False
        else:
            sk = table_name.split('_')[1]+'_sk' # remove 'dim_' prefix
            df.to_sql(name=table_name,
                      con=engine,
                      index=True,
                      index_label=sk,
                      chunksize=chunksize,
                      if_exists='append')
            conn.close()
            if(verbose):
                print('{} registries loaded.'.format(len(df)))
            return True

    def write_table(self, table_name, df, verbose=False):
        """Write dataframe to table.
        Parameters
        ----------
        table_name : str
            Table to be written

        df | Pandas DataFrame
            Data to be loaded

        verbose : boolean

        Returns
        -------
            status : boolean
                True on success, False otherwise
        """
        if(verbose):
            print('{}: '.format(table_name), end='', flush=True)

        ## psycopg2
        eng_str = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            self.user, self.pswd, self.host, self.port, self.base)
        engine = create_engine(eng_str)
        conn = self.get_conn()

        if conn == -1:
            print("ERROR: query(): Unable to connect to the database.")
            return False
        else:
            df.to_sql(name=table_name,
                      con=engine,
                      index=False,
                      if_exists='append')
            conn.close()
            if(verbose):
                print('{} registries loaded.'.format(len(df)))
            return True

    def query(self, query="SELECT"):
        """Connects to the Data Warehouse DB and run defined query

        Parameters
        ----------
            query : str
                Desired query

        Returns
        -------
            df : DataFrame
                Resulting Dataframe (Empty dataframe if unable to connect)
        """

        # Connect to an existing database
        conn = self.get_conn()

        if conn == -1:
            print("ERROR: query(): Unable to connect to the database.")
            return pd.DataFrame()

        # Perform query
        df = sqlio.read_sql_query(query, conn)

        # Close communication with the database
        conn.close()

        return df

if __name__ == '__main__':
    print('Data Warehouse Class')

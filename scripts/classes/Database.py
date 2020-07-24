from sqlalchemy import *


# Class for target database that overrides default sqlalchemy functionality with custom features.
# The most import feature here is the "replace_table" method which dynamically creates tables
# without the need for knowing and defining them beforehand.
class Database():

    def __init__(self, user, password, host, port, database_name, schema=None):
        self.ENGINE = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database_name}')
        self.METADATA = MetaData(self.ENGINE) if schema == None else MetaData(self.ENGINE, schema=schema)


    def create_schema(self, schema):
        """ Creates a schema within the database if it doesn't exists.

        :param schema:  Name of schema to be created.
        """
        try:
            self.ENGINE.execute(f'CREATE SCHEMA IF NOT EXISTS {schema};')
            print(f'{schema} created.')
            return True

        except Exception as err:
            print(err)
            return False


    def replace_table(self, schema, table_name, columns):
        """ Creates table within database with no constraints and all types as VARCHAR(250)
        Will delete table if it already exists in the target database.

        :param schema: Desired schema for table.
        :param table_name: Desired name for table.
        :param example_row: A dictionary containing keys that represent the table's columns
        """

        table = Table(table_name, self.METADATA, schema=schema)

        for column in columns:
            table.append_column(Column(column, VARCHAR(1000)))

        if self.ENGINE.dialect.has_table(self.ENGINE, table_name, schema=schema):
            self.ENGINE.execute(f"DROP TABLE {schema}.{table_name} CASCADE;")

        try:
            table.create()
            print(f"{table_name} created.")
            return True

        except Exception as err:
            print(err)
            return False


    def insert_into(self, schema, table_name, row):
        """ Inserts row into database

        :param schema: Name of schema to be inserted into.
        :param table_name: Name of table to be inserted into.
        :param row: A dictionary wherein keys represent columns and values represent values.
        Example for "row" argument -> {"column1": "value1", "column2": value2}
        Row dictionary must contain key, value pairs for every column in the target table.
        """

        table = Table(table_name, self.METADATA, autoload=True, schema=schema)
        insert_statement = table.insert()

        try:
            insert_statement.execute(row)
            return True

        except Exception as err:
            print(err)
            return False


    def get_raw_connection(self):
        return self.ENGINE.raw_connection()
# MAC env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2
import psycopg2
from database.tables import DatabaseTables
from logger.selenium_logger import logger
from config.config import config


class DbConnector:

    def __init__(self):
        self.__dbname = config.dbname
        self.__user = config.user
        self.__password = config.password
        self.__host = config.host
        self.__module = 'DbConnector'
        self.connection = psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password,
                                           host=self.__host)
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            #logger.info('{0}: PostgreSQL connection closed'.format(self.__module))

    def create_bot_table(self):
        table_sql = DatabaseTables.bot_table()
        self.cursor.execute(table_sql)
        self.connection.commit()

    def create_action_table(self):
        table_sql = DatabaseTables.action_table()
        self.cursor.execute(table_sql)
        self.connection.commit()

    def create_friends_table(self):
        table_sql = DatabaseTables.friends_table()
        self.cursor.execute(table_sql)
        self.connection.commit()

    def create_following_table(self):
        table_sql = DatabaseTables.following_table()
        self.cursor.execute(table_sql)
        self.connection.commit()

    def create_groups_table(self):
        table_sql = DatabaseTables.groups_table()
        self.cursor.execute(table_sql)
        self.connection.commit()

    def create_errors_table(self):
        table_sql = DatabaseTables.errors_table()
        self.cursor.execute(table_sql)
        self.connection.commit()

    def create_images_table(self):
        table_sql = DatabaseTables.images_table()
        self.cursor.execute(table_sql)
        self.connection.commit()

    def close(self):
        if (self.connection):
            self.cursor.close()
            self.connection.close()
            logger.info(
                '{0}: PostgreSQL connection closed'.format(self.__module))

    def roll_back(self):
        self.connection.rollback()

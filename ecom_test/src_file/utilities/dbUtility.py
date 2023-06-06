

import pymysql
import logging as logger
from ecom_test.src_file.utilities.credentialsUtility import CredentialsUtility
from ecom_test.src_file.config.MainConfigs import MainConfigs

# Define Class for Data base Connection
class DBUtility(object):

    def __init__(self):
        creds_helper = CredentialsUtility()
        self.creds = creds_helper.get_db_credentials()

        self.db_configs = MainConfigs.get_db_configs()
        self.host = self.db_configs['db_host']
        self.port = self.db_configs['port']
        self.database = self.db_configs['database']
        self.table_prefix = self.db_configs['table_prefix']

#Define class for creating DB connection
    def create_connection(self):
        connection = pymysql.connect(host=self.host, user=self.creds['db_user'],
                                     password=self.creds['db_password'],
                                     port=self.port)
        return connection

# to execute the connection

    def execute_select(self, sql):

        conn = self.create_connection()

        try:
            logger.debug(f"Executing: {sql}")
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchall()
            cur.close()
        except Exception as e:
            raise Exception(f"Failed running sql: {sql} \n  Error: {str(e)}")
        finally:
            conn.close()

        return rs_dict
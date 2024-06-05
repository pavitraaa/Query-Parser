"""
This script handles the connection to the various databases in our application.
"""

import mysql.connector
import redshift_connector
import config
from loguru import logger
from time import time
from utils.commons import json_map_generator


class MysqlDBInstance:
    """
    This class is used to perform necessary mysql database operations
    """

    # initializing the connection object which will return connection back to the calling api
    def __init__(self):
        self.connection = None
        self.cursor = None
        logger.add("logs/database_logs/mysql.log", level="DEBUG")

    # this method is used to create a connection to the mysql database
    def create_connection(self, schema):
        try:
            db_schema = schema
            if schema == "instacart":
                db_schema = "instacart1"
            # initializing the connection object with new database connection
            self.connection = mysql.connector.connect(
                host=config.mysql_db_conf["host"],
                port=config.mysql_db_conf["port"],
                user=config.mysql_db_conf["user"],
                password=config.mysql_db_conf["password"],
                database=db_schema
            )
            if self.connection and self.connection.is_connected():
                db_info = self.connection.get_server_info()
                logger.info("Mysql - Successfully connected to database:" + db_info)
                self.cursor = self.connection.cursor()
                logger.info("Mysql - Cursor successfully created")
        except mysql.connector.Error as err:
            error_map = {"error_no": err.errno, "error_msg": err.msg, "sqlstate": err.sqlstate}
            logger.error("Mysql - Error during connection to database: " + str(error_map))

    # this method is used to close a connection to the mysql database
    def close_connection(self):
        try:
            if self.connection and self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                logger.info("Mysql - Successfully closed the connection")
        except mysql.connector.Error as err:
            error_map = {"error_no": err.errno, "error_msg": err.msg, "sqlstate": err.sqlstate}
            logger.error("Mysql - Error during closing the database connection: " + str(error_map))

    # this method is used to execute a query in the mysql database
    def run_query(self, query):
        # storing the start time of the query
        start_time = 0
        # storing the end time of the query
        end_time = 0
        # storing the resultant query time
        query_time = ""
        try:
            if self.connection and self.connection.is_connected():
                start_time = int(round(time()*1000))
                self.cursor.execute(query)
                end_time = int(round(time()*1000))

                logger.debug("Mysql - Executed: " + query)

                query_time = str(end_time - start_time) + " ms"

                # storing column names to be returned back
                info = self.cursor.description
                columns = []
                for ind in range(len(info)):
                    columns.append(info[ind][0])

                # storing the results from the query
                results = []
                row = self.cursor.fetchone()
                cnt = 1
                while row and cnt<=2000:
                    results.append(json_map_generator(columns, row))
                    row = self.cursor.fetchone()
                    cnt+=1

                return "success", query, query_time, columns, results

        except mysql.connector.Error as err:
            error_map = {"error_no": err.errno, "error_msg": err.msg, "sqlstate": err.sqlstate}
            logger.error("Mysql - Error while executing query: " + query + " Error info: "+ str(error_map))
            return "failure", query, query_time, None, error_map

    # this method is used to commit the changes to the mysql database
    def commit(self):
        try:
            if self.connection and self.connection.is_connected():
                self.connection.commit()
                logger.info("Mysql - Committed the changes successfully")
        except mysql.connector.Error as err:
            error_map = {"error_no": err.errno, "error_msg": err.msg, "sqlstate": err.sqlstate}
            logger.error("Mysql - Error while committing changes: " + " Error info: " + str(error_map))


class RedshiftDBInstance:
    """
    This class is used to perform necessary redshift database operations
    """

    # initializing the connection object which will return connection back to the calling api
    def __init__(self):
        self.connection = None
        self.cursor = None
        logger.add("logs/database_logs/redshift.log", level="DEBUG")

    # this method is used to create a connection to the redshift database
    def create_connection(self, schema):
        try:
            db_schema = schema
            # initializing the connection object with new database connection
            self.connection = redshift_connector.connect(
                host='instabase-redshift.cw9pifbp7tf6.us-east-1.redshift.amazonaws.com',
                database=db_schema,
                user='awsuser',
                password='123Abcd!'
            )
            if self.connection:
                self.cursor = self.connection.cursor()
                logger.info("Redshift - Cursor successfully created")
        except redshift_connector.Error as err:
            error_map = {"error_code": err.args[0]["C"], "error_msg": err.args[0]["M"]}
            logger.error("Redshift - Error during connection to database: " + str(error_map))

    # this method is used to close a connection to the redshift database
    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
                self.connection.close()
                logger.info("Redshift - Successfully closed the connection")
        except redshift_connector.Error as err:
            error_map = {"error_code": err.args[0]["C"], "error_msg": err.args[0]["M"]}
            logger.error("Redshift - Error during closing the database connection: " + str(error_map))

    # this method is used to execute a query in the redshift database
    def run_query(self, query):
        # storing the start time of the query
        start_time = 0
        # storing the end time of the query
        end_time = 0
        # storing the resultant query time
        query_time = ""
        try:
            if self.cursor:
                start_time = int(round(time() * 1000))
                self.cursor.execute(query)
                end_time = int(round(time() * 1000))

                logger.debug("Redshift - Executed: " + query)

                query_time = str(end_time - start_time) + " ms"

                # storing column names to be returned back
                info = self.cursor.description
                columns = []
                for ind in range(len(info)):
                    columns.append(info[ind][0])

                # storing the results from the query
                results = []
                counter = 0
                row = self.cursor.fetchone()
                while row and counter<=2000:
                    results.append(json_map_generator(columns, row))
                    row = self.cursor.fetchone()
                    counter+=1

                return "success", query, query_time, columns, results

        except redshift_connector.Error as err:
            error_map = {"error_code": err.args[0]["C"], "error_msg": err.args[0]["M"]}
            logger.error("Redshift - Error while executing query: " + query + " Error info: " + str(error_map))
            return "failure", query, query_time, None, error_map

    # this method is used to commit the changes to the redshift database
    def commit(self):
        try:
            if self.connection and self.connection.is_connected():
                self.connection.commit()
                logger.info("Redshift - Committed the changes successfully")
        except redshift_connector.Error as err:
            error_map = {"error_code": err.args[0]["C"], "error_msg": err.args[0]["M"]}
            logger.error("Redshift - Error while committing changes: " + " Error info: " + str(error_map))
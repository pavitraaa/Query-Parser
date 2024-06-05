"""
This script handles loading of instacart csv data to AWS RDS.
"""

from utils.db_connector import MysqlDBInstance
from utils.schema_info import schemas, mysql_create_query, mysql_insert_map
import pandas as pd
from loguru import logger


class MysqlDataHandle:
    """
    this class handles all the necessary operations to load data into the AWS RDS mysql.
    """

    def __init__(self):
        logger.add("logs/dataload_logs/dataload.log", level="DEBUG")

    # this method is used to drop all the schemas pertaining to the application
    def drop_schema(self):
        db_ins = MysqlDBInstance()
        db_ins.create_connection()
        for sch in schemas:
            query = "drop table if exists " + sch
            db_ins.run_query(query)
        logger.info("Dropped all the schemas from the mysql database")
        db_ins.close_connection()

    # this method is used to create all the schemas pertaining to the application
    def create_schema(self):
        db_ins = MysqlDBInstance()
        db_ins.create_connection()
        for query in mysql_create_query:
            db_ins.run_query(query)
        logger.info("Created all the schemas into the mysql database")
        db_ins.close_connection()

    # this method is used to insert the data in the created schemas pertaining to the application
    def insert_data(self):
        db_ins = MysqlDBInstance()
        db_ins.create_connection()
        for sch, query in mysql_insert_map.items():
            data = pd.read_csv("resources/csv/"+sch+".csv", header=0).values.tolist()
            db_ins.cursor.executemany(query, data)
            logger.info("Inserted data into the schema:" + sch)
        logger.info("Inserted data to all the schemas in the mysql database")
        db_ins.commit()
        db_ins.close_connection()

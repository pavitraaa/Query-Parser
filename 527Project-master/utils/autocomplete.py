"""
This script is used to generate suggestions for sql keywords for MySQL and Redshift
"""

from utils.db_connector import MysqlDBInstance, RedshiftDBInstance
from utils.sql_keywords import generic_sql_keywords, mysql_keywords
from loguru import logger


class MysqlAutoComplete:
    """
    This class handles auto complete suggestions for Mysql database
    """

    def __init__(self):
        logger.add("logs/runtime_logs.log")
        self.completions = []
        self.load_suggestions()

    def load_suggestions(self):
        db_ins = MysqlDBInstance()
        db_ins.create_connection()
        query = """
        select table_name, column_name from information_schema.columns
        where table_schema = 'instacart'
        """
        state, time, columns, results = db_ins.run_query(query)
        if state == "success":
            table_names = set([table[0] for table in results])
            column_names = set([column[1] for column in results])
            result_names = table_names.union(column_names)
            self.completions = mysql_keywords + list(result_names)
            logger.info("Suggested MySQL keywords: " + str(self.completions))
        elif state == "failure":
            logger.error(results)
        db_ins.create_connection()

    def get_suggestions(self, prefix):
        prefix = prefix.lower()
        suggestions = filter(lambda x: x.lower().startswith(prefix), self.completions)
        suggestions = [suggestion for suggestion in suggestions]
        logger.info("Keyword suggestions: " + str(suggestions))
        return suggestions


class RedshiftAutoComplete:
    """
    This class handles auto complete suggestions for Redshift database
    """

    def __init__(self):
        logger.add("logs/runtime_logs.log")
        self.completions = []
        self.load_suggestions()

    def load_suggestions(self):
        db_ins = RedshiftDBInstance()
        db_ins.create_connection()
        query = """
        select table_name, column_name from information_schema.columns
        where table_schema='public' and table_catalog='instacart'
        """
        state, time, columns, results = db_ins.run_query(query)
        if state == "success":
            table_names = set([table[0] for table in results])
            column_names = set([column[1] for column in results])
            result_names = table_names.union(column_names)
            self.completions = generic_sql_keywords + list(result_names)
            logger.info("Suggested Redshift keywords: " + str(self.completions))
        elif state == "failure":
            logger.error(results)
        db_ins.create_connection()

    def get_suggestions(self, prefix):
        prefix = prefix.lower()
        suggestions = filter(lambda x: x.lower().startswith(prefix), self.completions)
        suggestions = [suggestion for suggestion in suggestions]
        logger.info("Keyword suggestions: " + str(suggestions))
        return suggestions

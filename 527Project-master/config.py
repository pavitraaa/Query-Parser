"""
This script consists of the necessary configuration setup for proper functioning of the application.
"""

# below set of configuration is to connect to the AWS RDS MySQL
mysql_db_conf = {
    "host" : "instabaserds.c16otsowwndg.us-east-1.rds.amazonaws.com",
    "port" : 3306,
    "user" : "admin",
    "password" : "123Abcd!"
}

# below set of configuration is to connect to the AWS Redshift
redshift_db_conf = {
    "host" : "instabase-redshift.cw9pifbp7tf6.us-east-1.redshift.amazonaws.com",
    "port" : 5439,
    "user" : "awsuser",
    "password" : "123Abcd!"
}
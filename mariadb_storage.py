##Functions inserting/deleting values into mariadb database

import pymysql.cursors

def insert_tempvalues(user, host, password, database, datetime, dict_tempvalues):
    """Insert  temperature values, sensor location from dict_tempvalues at the time of measurement datetime
    Inputs:
    -- user, host, password, database : information to connect to mariadb 
    -- datetime: time of grabbing data from sensors in format DATETIME
    -- dict_tempvalues: dict() containing temp values and sensor loc in format {loc: tempvalue}
    """
    connection = pymysql.connect(host = host,
                                 user = user,
                                 password = password,
                                 db = database,
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            for locid, tempvalue in dict_tempvalues.items():
                sql = "INSERT IGNORE INTO temperature (DateTime, TempC, LocId) VALUES (%s, %s, %s)"
                cursor.execute(sql, (datetime, tempvalue, locid))
        connection.commit()

        #with connection.cursor() as cursor:
         # Read a single record
         #   sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
         #   cursor.execute(sql, ('webmaster@python.org',))
         #   result = cursor.fetchone() print(result)
    finally:
        connection.close()


def insert_humvalues(user, host, password, database, datetime, dict_humvalues):
    """Insert humidity values, sensor location from dict_humvalues at the time of measurement datetime
    Inputs:
    -- user, host, password, database : information to connect to mariadb
    -- datetime: time of grabbing data from sensors in format DATETIME
    -- dict_humvalues: dict() containing humidity values and sensor loc in format {loc: humvalue}
    """
    connection = pymysql.connect(host = host,
                                 user = user,
                                 password = password,
                                 db = database,
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            for locid, humvalue in dict_humvalues.items():
                sql = "INSERT IGNORE INTO humidity (DateTime, HumidityPct, LocId) VALUES (%s, %s, %s)"
                cursor.execute(sql, (datetime, humvalue, locid))
        connection.commit()

    finally:
        connection.close()


def limit_tempvalues(user, host, password, database, max_values = 100000):
    """Delete the oldest recordings when number of rows exceeds max_values in the table temperature"""
    connection = pymysql.connect(host = host,
                                 user = user,
                                 password = password,
                                 db = database,
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Delete oldest rows if their number exceed max_values
            sql = "DELETE FROM temperature WHERE DateTime NOT IN (SELECT * FROM (SELECT Datetime FROM temperature ORDER BY DateTime DESC LIMIT 0, %s) as t);"
            cursor.execute(sql, (max_values))

        connection.commit()
    finally:
        connection.close() 


def limit_humvalues(user, host, password, database, max_values = 35000):
    """Delete the oldest recordings when number of rows exceeds max_values in the table humidity"""
    connection = pymysql.connect(host = host,
                                 user = user,
                                 password = password,
                                 db = database,
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Delete oldest rows if their number exceed max_values
            sql = "DELETE FROM humidity WHERE DateTime NOT IN (SELECT * FROM (SELECT Datetime FROM humidity ORDER BY DateTime DESC LIMIT 0, %s) as t);"
            cursor.execute(sql, (max_values))

        connection.commit()
    finally:
        connection.close()


def clear_table(user, host, password, database, table):
    """Empty desired table from database
    Inputs:
    -- user, host, password, database : information to connect to mariadb 
    -- table : table to empty
    """
    connection = pymysql.connect(host = host,
                                 user = user,
                                 password = password,
                                 db = database,
                                 charset = 'utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
             cursor.execute("TRUNCATE %s" %(table))
        connection.commit()

    finally:
        connection.close()


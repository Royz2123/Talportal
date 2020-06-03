import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='admin', password='password', database='moodle')
cursor = mariadb_connection.cursor()
cursor.execute('select * from mdl_user;')
for user in cursor:
    print(user)


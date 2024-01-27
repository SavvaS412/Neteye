import mysql.connector
import re

DB_NAME = 'netEye'

DEVICES_TABLE_NAME = 'devices'
DEVICES_COL_ID = 'id'
DEVICES_COL_NAME = 'name'
DEVICES_COL_IP = 'ip'
DEVICES_COL_MAC = 'mac'
DEVICES_COL_IS_AVAILABLE = 'isAvailable'

NOTIFICATIONS_TABLE_NAME = 'notifications'
NOTIFICATIONS_COL_ID = 'id'
NOTIFICATIONS_COL_NAME = 'name'
NOTIFICATIONS_COL_TYPE = 'type'
NOTIFICATIONS_COL_DESCRIPTION = 'description'
NOTIFICATIONS_COL_DATE = 'date'
NOTIFICATIONS_COL_IS_READ = 'isRead'

RULES_TABLE_NAME = 'rules'
RULES_COL_ID = 'id'
RULES_COL_NAME = 'name'
RULES_COL_ACTION = 'action'
RULES_COL_PARAMETER = 'parameter'
RULES_COL_AMOUNT = 'amount'
RULES_COL_TARGET_DEVICE = 'target ip'

EMAILS_TABLE_NAME = 'emails'
EMAILS_COL_ID = 'id'
EMAILS_COL_EMAIL = 'email'

def create_table_if_not_exists(cursor, table_name, table_definition):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    if not cursor.fetchone():
        cursor.execute(table_definition)

def is_devices_table(cursor):
    create_table_if_not_exists(cursor, DEVICES_TABLE_NAME, f'''
            CREATE TABLE {DEVICES_TABLE_NAME} ( 
            {DEVICES_COL_ID} INT AUTO_INCREMENT PRIMARY KEY,
            {DEVICES_COL_NAME} VARCHAR(255),
            {DEVICES_COL_IP} VARCHAR(15),
            {DEVICES_COL_MAC} VARCHAR(17),
            {DEVICES_COL_IS_AVAILABLE} BOOL)
    ''')

def is_notifications_table(cursor):
    create_table_if_not_exists(cursor, NOTIFICATIONS_TABLE_NAME, f'''
        CREATE TABLE {NOTIFICATIONS_TABLE_NAME} (
            {NOTIFICATIONS_COL_ID} INT AUTO_INCREMENT PRIMARY KEY,
            {NOTIFICATIONS_COL_NAME} VARCHAR(255),
            {NOTIFICATIONS_COL_TYPE} VARCHAR(255),
            {NOTIFICATIONS_COL_DESCRIPTION} TEXT,
            {NOTIFICATIONS_COL_DATE} DATETIME,
            {NOTIFICATIONS_COL_IS_READ} BOOL)
    ''')

def is_rules_table(cursor):
    create_table_if_not_exists(cursor, RULES_TABLE_NAME, f'''
        CREATE TABLE {RULES_TABLE_NAME} (
            {RULES_COL_ID} INT AUTO_INCREMENT PRIMARY KEY,
            {RULES_COL_NAME} VARCHAR(255),
            {RULES_COL_ACTION} INT,
            {RULES_COL_PARAMETER} INT,
            {RULES_COL_AMOUNT} INT),
            {RULES_COL_TARGET_DEVICE} TEXT)
    ''')

def is_emails_table(cursor):
    create_table_if_not_exists(cursor, EMAILS_TABLE_NAME, f'''
        CREATE TABLE {EMAILS_TABLE_NAME} (
            {EMAILS_COL_ID} INT AUTO_INCREMENT PRIMARY KEY,
            {EMAILS_COL_EMAIL} VARCHAR(255) UNIQUE)
    ''')

def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='admin',
        password='admin',
        database=DB_NAME)

def create_database():
    try:
        with mysql.connector.connect(host='localhost',user='admin',password='admin') as conn:
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')

    except Exception as e:
        print(f"Error creating database: {e}")

def insert_rule(name, parameter, action, amount, target):
    try:
        with connect_to_db() as conn:
            cursor = conn.cursor()

            insert_query = f'''
                INSERT INTO {RULES_TABLE_NAME} 
                ({RULES_COL_NAME}, {RULES_COL_PARAMETER}, {RULES_COL_ACTION}, {RULES_COL_AMOUNT}, {RULES_COL_TARGET_DEVICE})
                VALUES (%s, %s, %s, %s, %s)'''

            cursor.execute(insert_query, (name, parameter, action, amount, target))
            conn.commit()
            print("Rule inserted successfully!")

    except Exception as e:
        print(f"Error inserting rule: {e}")

def print_mails_table(cursor):
    try:
        cursor.execute("SELECT * FROM mails_table")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, Mail: {row[1]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def is_valid_email(email):
    # Use a regular expression to check if the email format is valid
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def insert_mail(cursor, conn):
    try:
        new_mail = input("Enter the email to add to the table: ")
        
        if not is_valid_email(new_mail):
            print("Invalid email format. Please enter a valid email.")
            return
        
        insert_query = f"INSERT INTO {EMAILS_TABLE_NAME} (mail) VALUES (%s)"
        cursor.execute(insert_query, (new_mail,))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def remove_mail(cursor):

def changes_in_mails_table(cursor, conn):
    choice = -1
    while(choice != 0):
        print_mails_table(cursor)
        while(not (0 <= choice <= 2)):
            choice = input("Which action would you like to do? \n0. Exit. \n1. Insert mail. \n2. Remove mail.")
        
        if(choice == 1):
            insert_mail(cursor, conn)

        if(choice == 2):
            remove_mail(cursor)

        print()


def main():
    create_database()

    with connect_to_db() as conn:
        cursor = conn.cursor()

        is_devices_table(cursor)
        is_notifications_table(cursor)
        is_rules_table(cursor)
        is_emails_table(cursor)

        insert_rule('Sample Rule', 1, 2, 100)

        changes_in_mails_table(cursor, conn)

if __name__ == '__main__':
    main()

import pymssql
import logging
import configparser

# Prepare configparser
config = configparser.ConfigParser()
config.read('config.ini')

# SQL login credentials
server = config['DEFAULT']['server']
user = config['DEFAULT']['user']
password = config['DEFAULT']['password']
db = config['DEFAULT']['db']


# retrieve store information from SQL
def get_store_list():

    store_list = []
    attempts = 0

    while attempts < 3:
        try:

            # Create connection to server
            conn = pymssql.connect(server, user, password, db)

            # return each row in result as a dict
            cursor = conn.cursor(as_dict=True)

            # Grab stores
            cursor.execute('Staging.usp_Get_Store_Data')

            logging.info('Retrieving store data.')

            for row in cursor:
                store_list.append(row)

            # Gracefully close connection
            conn.close()
            logging.info('Store data retrieved.')

            return store_list

        except Exception as e:

            # log exception
            logging.error('Failed to retrieve store data. Exception: %s' % str(e))

            # increase attempt counter
            attempts += 1

    # log failure
    logging.error('Exiting application prematurely.')

    # exit application
    quit()


# update information for specific store
def update_store(storecode):

    attempts = 0

    while attempts < 3:
        try:

            # Create connection to server
            conn = pymssql.connect(server, user, password, db)

            # return each row in result as a dict
            cursor = conn.cursor(as_dict=True)

            # Grab stores
            cursor.execute('Staging.usp_Get_Store_Data %s' % storecode)
            updated_store = cursor.fetchone()

            # Gracefully close connection
            conn.close()

            return updated_store

        except Exception as e:

            # log exception
            logging.error('Failed to update store data.')
            logging.error('Exception: ' + str(e))

            # increase attempt counter
            attempts += 1

    # log failure
    logging.error('Exiting application prematurely.')

    # exit application
    quit()


def insert_xml(insert_values):

    insert_string = "INSERT INTO Staging.Documents (Store_Code, Document_Type, Document_Text) VALUES (%s, %s, %s)"
    attempts = 0

    while attempts < 3:
        try:

            # create connection and cursor
            conn = pymssql.connect(server, user, password, db)
            cursor = conn.cursor()

            # bulk insert list of tuples
            cursor.executemany(insert_string, insert_values)

            # must commit unless auto-commit is enabled (it's not)
            conn.commit()

            # close connection gracefully
            conn.close()

            return

        except Exception as e:

            # log exception
            logging.error('Failed to insert data. Exception: %s' % str(e))

            # increase attempt counter
            attempts += 1

    # log failure
    logging.error('Exiting application prematurely.')

    # exit application
    quit()


def run_import_process():

    logging.info('Import stored proc started.')

    attempts = 0

    while attempts < 3:
        try:

            # Create connection to server
            conn = pymssql.connect(server, user, password, db)

            # return each row in result as a dict
            cursor = conn.cursor(as_dict=True)

            # Run proc
            cursor.callproc('Staging.usp_Run_Import')

            # Gracefully close connection
            conn.close()
            logging.info('Import stored proc executed.')

        except Exception as e:

            # log exception
            logging.error('Failed to execute stored proc. Exception: %s' % str(e))

            # increase attempt counter
            attempts += 1

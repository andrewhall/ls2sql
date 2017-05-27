import pymssql
import logging

# SQL login credentials
server = '25.15.227.115'
user = 'Lightspeed'
password = 'Lightspeed123'
db = 'Staging'


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
            logging.error('Failed to retrieve store data: ' + str(e))

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
            logging.error('Failed to update store data: ' + str(e))

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
            logging.error('Failed to insert data: ' + str(e))

            # increase attempt counter
            attempts += 1

    # log failure
    logging.error('Exiting application prematurely.')

    # exit application
    quit()

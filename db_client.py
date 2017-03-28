import pymssql
import logging

# SQL login credentials
server = '25.15.227.115'
user = 'Lightspeed'
password = 'Lightspeed123'
db = 'Staging'


# retrieve store information from SQL
def get_store_list():
    logging.info('Retrieving store data.')

    store_list = []
    conn = pymssql.connect(server, user, password, db)

    # return each row in result as a dict
    cursor = conn.cursor(as_dict=True)

    # only grabbing stores with sync = 1 flag
    cursor.execute('Staging.usp_Get_Store_Data')
    for row in cursor:
        store_list.append(row)

    # Gracefully close connection
    conn.close()
    logging.info('Store data retrieved.')

    return store_list


def insert_xml(insert_values):

    insert_string = "INSERT INTO Staging.Documents_test (Store_Code, Document_Type, Document_Text) VALUES (%s, %s, %s)"

    # create connection and cursor
    conn = pymssql.connect(server, user, password, db)
    cursor = conn.cursor()

    # bulk insert list of tuples
    cursor.executemany(insert_string, insert_values)

    # must commit unless auto-commit is enabled (it's not)
    conn.commit()

    # close connection gracefully
    conn.close()

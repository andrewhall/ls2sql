import pymssql, logging

# SQL login credentials
server = '25.15.227.115'
user = 'Lightspeed'
password = 'Lightspeed123'
db = 'Staging'


def get_store_list():
    logging.info('Retrieving store data.')

    #
    store_list = []
    conn = pymssql.connect(server, user, password, db)
    cursor = conn.cursor(as_dict=True)
    cursor.execute('SELECT * FROM Staging.lightspeed_stores')
    for row in cursor:
        store_list.append(row)
    conn.close()
    logging.info('Store data retrieved.')
    return store_list



# def insert_xml(invoices):
#     conn = pymssql.connect(server, user, password, db)
#     cursor = conn.cursor()
#
#     for invoice in invoices:
#         cursor.execute('''
#             INSERT INTO LIGHTSPEED_INVOICES
#             (invoice_id, storecode, document_id,
#             friendly_id, datetime_created, datetime_modified,
#             customer, margin, primary_user,
#             secondary_user, subtotal, tax,
#             total, owing, paid)
#             VALUES
#             (%(invoice_id)s, %(storecode)s, %(document_id)s,
#             %(friendly_id)s, %(datetime_created)s, %(datetime_modified)s,
#             %(customer)s, %(margin)s, %(primary_user)s,
#             %(secondary_user)s, %(subtotal)s, %(tax)s,
#             %(total)s, %(owing)s, %(paid)s)''', invoice.data)
#         conn.commit()
#         cursor.execute('''UPDATE LIGHTSPEED_STORES
#                           SET last_invoice = %(invoice_id)s
#                           WHERE storecode = %(storecode)s;''', invoice.data)
#         conn.commit()
#
#     conn.close()

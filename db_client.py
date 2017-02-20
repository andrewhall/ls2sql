import pymssql, logging

# SQL login credentials
server = '25.15.227.115'
user = 'Lightspeed'
password = 'Lightspeed123'
db = 'Staging'


def get_store_list():
    logging.info('Retrieving store data.')

    store_list = []
    conn = pymssql.connect(server, user, password, db)
    cursor = conn.cursor(as_dict=True)
    cursor.execute('SELECT * FROM Staging.lightspeed_stores')
    for row in cursor:
        store_list.append(row)
    conn.close()
    logging.info('Store data retrieved.')
    return store_list


def insert_xml(store, type, xml):
    columns = { 'invoice': 'last_invoice_id',
                'products': 'last_product-id',
                'purchase_order': 'last_purchase_order',
                'supplier': 'last_supplier_id',
                'customer': 'last_customer_id',
                'user': 'last_user_id'}

    conn = pymssql.connect(server, user, password, db)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Staging.Documents
        (Store_Code, Document_Type, Document_Text)
        VALUES
        (?, ?, ?)''', store, type, xml)
    conn.commit()


    cursor.execute('''UPDATE Staging.lightspeed_stores
                      SET last_invoice = %(invoice_id)s
                      WHERE storecode = %(storecode)s;''', invoice.data)
    conn.commit()

    conn.close()

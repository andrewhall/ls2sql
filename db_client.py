import pymssql, logging

server = '25.15.227.115'
user = 'Lightspeed'
password = 'Lightspeed123'
db = 'Lightspeed'


def get_store_list():
    store_list = []
    conn = pymssql.connect(server, user, password, db)
    cursor = conn.cursor(as_dict=True)
    cursor.execute('SELECT * FROM LIGHTSPEED_STORES')
    for row in cursor:
        store_list.append(row)
    conn.close()
    return store_list


def insert_invoices(invoices):
    conn = pymssql.connect(server, user, password, db)
    cursor = conn.cursor()

    for invoice in invoices:
        cursor.execute('''
            INSERT INTO LIGHTSPEED_INVOICES
            (invoice_id, storecode, document_id,
            friendly_id, datetime_created, datetime_modified,
            customer, margin, primary_user,
            secondary_user, subtotal, tax,
            total, owing, paid)
            VALUES
            (%(invoice_id)s, %(storecode)s, %(document_id)s,
            %(friendly_id)s, %(datetime_created)s, %(datetime_modified)s,
            %(customer)s, %(margin)s, %(primary_user)s,
            %(secondary_user)s, %(subtotal)s, %(tax)s,
            %(total)s, %(owing)s, %(paid)s)''', invoice.data)
        conn.commit()
        cursor.execute('''UPDATE LIGHTSPEED_STORES
                          SET last_invoice = %(invoice_id)s
                          WHERE storecode = %(storecode)s;''', invoice.data)
        conn.commit()

    conn.close()


def insert_lineitems(lineitems):
    conn = pymssql.connect(server, user, password, db)
    cursor = conn.cursor()

    for lineitem in lineitems:
        cursor.execute('''
            INSERT INTO LIGHTSPEED_LINEITEMS
            (lineitem_id, storecode, parent_id,
            code, description, quantity,
            sell_price, sell, base,
            total, class_name, class_id,
            family_name, product_id, notes,
            available, cost, margin, profit_margin)
            VALUES
            (%(lineitem_id)s, %(storecode)s, %(parent_id)s,
            %(code)s, %(description)s, %(quantity)s,
            %(sell_price)s, %(sell)s, %(base)s,
            %(total)s, %(class_name)s, %(class_id)s,
            %(family_name)s, %(product_id)s, %(notes)s,
            %(available)s, %(cost)s, %(margin)s, %(profit_margin)s)''', lineitem.data)
        conn.commit()
        cursor.execute('''UPDATE LIGHTSPEED_STORES
                          SET last_lineitem = %(lineitem_id)s
                          WHERE storecode = %(storecode)s;''', lineitem.data)
        conn.commit()
    conn.close()


def insert_customer(customers):
    conn = pymssql.connect(server, user, password, db)
    cursor = conn.cursor()

    for customer in customers:
        cursor.execute('''
            INSERT INTO LIGHTSPEED_CUSTOMERS
            (customer_id, storecode, first_name, last_name, company, email)
            VALUES
            (%(customer_id)s, %(storecode)s, %(first_name)s, %(last_name)s, %(company)s, %(email)s)''', customer.data)
        conn.commit()
        cursor.execute('''UPDATE LIGHTSPEED_STORES
                          SET last_customer = %(customer_id)s
                          WHERE storecode sto= %(storecode)s;''', customer.data)
        conn.commit()
    conn.close()

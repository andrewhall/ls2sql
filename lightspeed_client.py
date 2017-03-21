import requests, logging, db_client
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xml.etree import ElementTree


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {'User-Agent': 'com.sunsetnovelties.invoices/1.0',
           'X-PAPPID': 'ee18ea41-2705-4189-b628-095d995d0d33',
           'Content-Type': 'text/xml'}


def process_store(current_store):
    logging.info('%s: Store initiating.' % current_store['store'])

    imbed_invoices(current_store)
    capture_customers(current_store)
    unite_users(current_store)
    salvage_suppliers(current_store)
    procure_purchase_orders(current_store)
    produce_products(current_store)

    logging.info('%s: Store completed.' % current_store['store'])


def imbed_invoices(current_store):

    invoice_list = []
    start = 0
    end = 250
    invoice_filter = {'filter': 'id > \"%s\" AND id <= \"%s\"' % (start, end)}
    invoice_url = current_store['address'] + 'invoices/'
    response = requests.get(invoice_url,
                            params=invoice_filter,
                            auth=(current_store['username'], current_store['password']),
                            headers=headers,
                            verify=False)
    root = ElementTree.fromstring(response.text)
    for child in root:
        invoice_uri = child.get('uri')
        invoice_list.append(invoice_uri)

    insert_values = []

    for invoice in invoice_list:
        response = requests.get(invoice,
                                auth=(current_store['username'], current_store['password']),
                                headers=headers,
                                verify=False)
        root = ElementTree.fromstring(response.text)

        temp_values = (current_store['storecode'], root.tag, ElementTree.tostring(root))

        insert_values.append(temp_values)

    db_client.insert_xml(insert_values)


def capture_customers(current_store):

    logging.info('%s: Customer data initiating.' % current_store['store'])

    invoice_url = current_store['address'] + 'customers/'

    response = requests.get(invoice_url,
                            auth=(current_store['username'], current_store['password']),
                            headers=headers,
                            verify=False)
    root = ElementTree.fromstring(response.text)

    insert_values = [(current_store['storecode'], root.tag, ElementTree.tostring(root))]

    db_client.insert_xml(insert_values)

    logging.info('%s: Customer data completed.' % current_store['store'])


def unite_users(current_store):

    logging.info('%s: User data initiating.' % current_store['store'])

    invoice_url = current_store['address'] + 'users/'

    response = requests.get(invoice_url,
                            auth=(current_store['username'], current_store['password']),
                            headers=headers,
                            verify=False)
    root = ElementTree.fromstring(response.text)

    insert_values = [(current_store['storecode'], root.tag, ElementTree.tostring(root))]

    db_client.insert_xml(insert_values)

    logging.info('%s: User data completed.' % current_store['store'])


def salvage_suppliers(current_store):

    logging.info('%s: Supplier data initiating.' % current_store['store'])

    invoice_url = current_store['address'] + 'suppliers/'

    response = requests.get(invoice_url,
                            auth=(current_store['username'], current_store['password']),
                            headers=headers,
                            verify=False)
    root = ElementTree.fromstring(response.text)

    insert_values = [(current_store['storecode'], root.tag, ElementTree.tostring(root))]

    db_client.insert_xml(insert_values)

    logging.info('%s: Supplier data completed.' % current_store['store'])


def procure_purchase_orders(current_store):

    logging.info('%s: PO data initiating.' % current_store['store'])

    po_list = []
    start = 0
    end = 250
    po_filter = {'filter': 'id > \"%s\" AND id <= \"%s\"' % (start, end)}
    po_url = current_store['address'] + 'purchase_orders/'
    response = requests.get(po_url,
                            params=po_filter,
                            auth=(current_store['username'], current_store['password']),
                            headers=headers,
                            verify=False)
    root = ElementTree.fromstring(response.text)
    for child in root:
        po_uri = child.get('uri')
        po_list.append(po_uri)

    insert_values = []

    for po in po_list:
        response = requests.get(po,
                                auth=(current_store['username'], current_store['password']),
                                headers=headers,
                                verify=False)
        root = ElementTree.fromstring(response.text)

        temp_values = (current_store['storecode'], root.tag, ElementTree.tostring(root))

        insert_values.append(temp_values)

    db_client.insert_xml(insert_values)

    logging.info('%s: PO data completed.' % current_store['store'])


def produce_products(current_store):

    logging.info('%s: Product data initiating.' % current_store['store'])

    invoice_url = current_store['address'] + 'products/'

    response = requests.get(invoice_url,
                            auth=(current_store['username'], current_store['password']),
                            headers=headers,
                            verify=False)
    root = ElementTree.fromstring(response.text)

    insert_values = [(current_store['storecode'], root.tag, ElementTree.tostring(root))]

    db_client.insert_xml(insert_values)

    logging.info('%s: Product data completed.' % current_store['store'])
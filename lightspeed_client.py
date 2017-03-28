import requests
import logging
import db_client
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xml.etree import ElementTree

# suppress warning about not verifying SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def process_store(current_store):
    logging.info('%s | Store initiating.' % current_store['store'])

    # Create persistent API session
    session = requests.Session()
    session.verify = False
    session.auth = (current_store['username'], current_store['password'])
    session.headers.update({'User-Agent': 'com.sunsetnovelties.invoices/1.0',
                            'X-PAPPID': 'ee18ea41-2705-4189-b628-095d995d0d33',
                            'Content-Type': 'text/xml'})

    # Do work, bitch
    process_summary_records(current_store, session)
    process_detailed_records(current_store, session)

    # Close API session gracefully
    session.close()

    logging.info('%s | Store completed.' % current_store['store'])


# def imbed_invoices(current_store, session):
#
#     logging.info('%s: Invoice data initiating.' % current_store['store'])
#
#     invoice_list = []
#     invoice_filter = {'filter': 'id > \"%s\" AND id <= \"%s\"' % (current_store['last_invoice'],
#                                                                   current_store['last_invoice'] + 250)}
#     response = session.get(current_store['address'] + 'invoices/', params=invoice_filter)
#
#     root = ElementTree.fromstring(response.text)
#
#     for child in root:
#         invoice_uri = child.get('uri')
#         invoice_list.append(invoice_uri)
#
#     insert_values = []
#
#     for invoice in invoice_list:
#         response = session.get(invoice)
#
#         root = ElementTree.fromstring(response.text)
#
#         temp_values = (current_store['storecode'], root.tag, ElementTree.tostring(root))
#
#         insert_values.append(temp_values)
#
#     db_client.insert_xml(insert_values)
#
#     logging.info('%s: Invoice data completed.' % current_store['store'])
#

# def procure_purchase_orders(current_store):
#
#     logging.info('%s: PO data initiating.' % current_store['store'])
#
#     po_list = []
#     start = 0 # fix start and end here
#     end = 250
#     po_filter = {'filter': 'id > \"%s\" AND id <= \"%s\"' % (start, end)}
#     po_url = current_store['address'] + 'purchase_orders/'
#     response = requests.get(po_url,
#                             params=po_filter,
#                             auth=(current_store['username'], current_store['password']),
#                             headers=headers,
#                             verify=False)
#     root = ElementTree.fromstring(response.text)
#     for child in root:
#         po_uri = child.get('uri')
#         po_list.append(po_uri)
#
#     insert_values = []
#
#     for po in po_list:
#         response = requests.get(po,
#                                 auth=(current_store['username'], current_store['password']),
#                                 headers=headers,
#                                 verify=False)
#         root = ElementTree.fromstring(response.text)
#
#         temp_values = (current_store['storecode'], root.tag, ElementTree.tostring(root))
#
#         insert_values.append(temp_values)
#
#     db_client.insert_xml(insert_values)
#
#     logging.info('%s: PO data completed.' % current_store['store'])
#
#

def process_summary_records(current_store, session):

    # types of records processed in this method
    document_types = ['customers', 'users', 'suppliers', 'products']

    # Loop through
    for document_type in document_types:

        logging.info('%s | Initiating: %s data.' % (current_store['storecode'], document_type))

        response = session.get(current_store['address'] + document_type + '/')

        root = ElementTree.fromstring(response.text)

        insert_values = [(current_store['storecode'], root.tag, ElementTree.tostring(root))]

        db_client.insert_xml(insert_values)

        logging.info('%s | Completed: %s data.' % (current_store['storecode'], document_type))


def process_detailed_records(current_store, session):

    # types of records processed in this method
    document_types = ['invoices', 'purchase_orders']
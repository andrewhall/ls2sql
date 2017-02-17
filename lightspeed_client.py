import requests, logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xml.etree import ElementTree

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {'User-Agent': 'com.sunsetnovelties.invoices/1.0',
           'X-PAPPID': 'ee18ea41-2705-4189-b628-095d995d0d33',
           'Content-Type': 'text/xml'}

def process_store(current_store):
    logging.info('%s initiating.' % store['store'])

    logging.info('%s completed.' % store['store'])

# def get_invoice_list(current_store):
#     invoice_list = []
#     start = current_store['last_invoice']
#     end = start + 100
#     invoice_filter = {'filter': 'id > \"%s\" AND id <= \"%s\"' % (start, end)}
#     invoice_url = current_store['address'] + 'invoices/'
#     response = requests.get(invoice_url,
#                             params=invoice_filter,
#                             auth=(current_store['username'], current_store['password']),
#                             headers=headers,
#                             verify=False)
#     root = ElementTree.fromstring(response.text)
#     for child in root:
#         invoice_id = child.get('uri')
#         invoice_list.append(invoice_id)
#
#     current_store['last_invoice'] = end
#     return invoice_list
#
#
# def get_invoice(uri):
#     response = requests.get(uri,
#                             auth=('LIGHTSPEED', 'SUNSET69!'),
#                             headers=headers,
#                             verify=False)
#     tree = ElementTree.fromstring(response.text)
#     return Invoice(tree)
#
#
# def get_lineitem(uri):
#     response = requests.get(uri,
#                             auth=('LIGHTSPEED', 'SUNSET69!'),
#                             headers=headers,
#                             verify=False)
#     tree = ElementTree.fromstring(response.text)
#     return Lineitem(tree)
#
#
# def build_invoices(invoice_list):
#     invoices = []
#     for item in invoice_list:
#         invoices.append(get_invoice(item))
#     return invoices
#
#
# def build_lineitems(invoices):
#     lineitems = []
#     for invoice in invoices:
#         for lineitem in invoice.data['lineitems']:
#             temp_lineitem = get_lineitem(lineitem)
#             temp_lineitem.data['storecode'] = invoice.data['storecode']
#             temp_lineitem.data['parent_id'] = invoice.data['invoice_id']
#             lineitems.append(temp_lineitem)
#
#     return lineitems

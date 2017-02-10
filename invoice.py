class Invoice:
    def __init__(self, tree):
        self.data = {'invoice_id': tree.get('id'),
                     'storecode': tree.find('storecode').text,
                     'document_id': tree.find('document_id').text,
                     'datetime_created': tree.find('datetime_created').text,
                     'datetime_modified': tree.find('datetime_modified').text,
                     'friendly_id': tree.find('invoice_id').text,
                     'customer': tree.find('invoice_customer').find('customer').get('id'),
                     'margin': tree.find('margin').text,
                     'primary_user': tree.find('primary_user').find('user').get('id'),
                     'secondary_user': tree.find('secondary_user').find('user').get('id'),
                     'subtotal': tree.find('totals').find('subtotal').text,
                     'tax': tree.find('totals').find('tax').text,
                     'total': tree.find('totals').find('total').text,
                     'owing': tree.find('totals').find('owing').text,
                     'paid': tree.find('totals').find('paid').text,
                     'lineitems': []}
        for item in tree.iter('lineitem'):
            self.data['lineitems'].append(item.get('uri'))

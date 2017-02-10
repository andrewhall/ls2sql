class Lineitem:
    def __init__(self, tree):
        self.data = {'lineitem_id': tree.get('id'),
                     'storecode': '',
                     'parent_id': 0,
                     'code': tree.find('lineitem_product').find('code').text,
                     'description': tree.find('lineitem_product').find('description').text,
                     'quantity': tree.find('quantity').text,
                     'sell_price': tree.find('sell_price').text,
                     'sell': tree.find('sells').find('sell').text,
                     'base': tree.find('sells').find('base').text,
                     'total': tree.find('sells').find('total').text,
                     'class_name': tree.find('lineitem_product').find('class_name').text,
                     'class_id': tree.find('lineitem_product').find('product').find('class').get('id'),
                     'family_name': tree.find('lineitem_product').find('family').text,
                     'product_id': tree.find('lineitem_product').find('product').find('product_id').text,
                     'notes': tree.find('lineitem_product').find('product').find('notes').text,
                     'available': tree.find('lineitem_product').find('product')
                                 .find('inventory').find('available').text,
                     'cost': tree.find('cost').get('total'),
                     'margin': tree.find('lineitem_product').find('product').find('margin').text,
                     'profit_margin': tree.find('profit_margin').text}

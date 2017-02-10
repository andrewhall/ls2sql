class Customer:
    def __init__(self, tree):
        self.data = {'customer_id': tree.get('id'),
                     'storecode': 'NOT SET',
                     'first_name': tree.find('name').find('first').text,
                     'last_name': tree.find('name').find('last').text,
                     'company': tree.find('company').text,
                     'email': tree.find('email').text}

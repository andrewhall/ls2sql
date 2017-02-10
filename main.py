import time
import lightspeed_client
import mom_client

stores = mom_client.get_store_list()
print('*** STORE LIST CREATED ***', end='\n\n')

for store in stores:

    while True:
        print('*** STORE: %s | START TIME: %s' % (store['store'], time.strftime("%H:%M:%S")))

        if store['storecode'] == 'MAIN':
            break

        print('* GENERATING INVOICE LIST')
        start = time.time()
        invoice_list = lightspeed_client.get_invoice_list(store)
        if len(invoice_list) == 0:
            break
        print('** %d INVOICES TO RETRIEVE' % len(invoice_list))

        invoices = lightspeed_client.build_invoices(invoice_list)
        print('* BUILDING INVOICES: COMPLETE')

        lineitems = lightspeed_client.build_lineitems(invoices)
        print('* BUILDING LINEITEMS: COMPLETE ')

        mom_client.insert_invoices(invoices)
        print('* INSERTING INVOICES: COMPLETE')

        mom_client.insert_lineitems(lineitems)
        print('* INSERTING LINEITEMS: COMPLETE')

        duration = time.time()-start
        print('*** BATCH DURATION: %s' % time.strftime('%H:%M:%S', time.gmtime(duration)), end='\n\n')

    print('*** %s COMPLETE ***' % store['store'], end='\n\n')


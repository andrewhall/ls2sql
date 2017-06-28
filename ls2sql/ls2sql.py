import lightspeed_client
import db_client
import logging
import time

version = '1.0.0'

# format logging output
log_datetime = time.strftime("%m%d")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='../logs/ls2sql_' + log_datetime + '.log',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


def main():
    logging.info('Application started. Version: %s' % version)

    # Retrieve all store information
    stores = db_client.get_store_list()

    # Loop through stores to process
    for store in stores:
        lightspeed_client.process_store(store)

    # Process new XML records
    # db_client.run_import_process()

    logging.info('Application ended.')

if __name__ == '__main__':
    main()

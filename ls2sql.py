import lightspeed_client
import db_client
import logging
import time

# format logging output
log_datetime = time.strftime("%m%d")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='ls2sql_' + log_datetime + '.log',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


def main():
    logging.info('Application started.')

    # Retrieve all store information
    stores = db_client.get_store_list()

    # Loop through stores to process
    for store in stores:
        lightspeed_client.process_store(store)

    logging.info('Application ended.')

if __name__ == '__main__':
    main()

attempts = 0

# while attempts < 3:
#     try:
#
#
#
#     except Exception as e:
#
#         # log exception
#         logging.error('Failed to retrieve %s data: ' + str(e) % document_type)
#
#         # increase attempt counter
#         attempts += 1
#
#         continue

import requests
import logging
import db_client
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xml.etree import ElementTree

# suppress warning about not verifying SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def process_store(current_store):
    logging.info('%s | Store initiated.' % current_store['store'])

    # Create persistent API session
    session = requests.Session()
    session.verify = False
    session.timeout = 10
    session.auth = (current_store['username'], current_store['password'])
    session.headers.update({'User-Agent': 'com.sunsetnovelties.invoices/1.0',
                            'X-PAPPID': 'ee18ea41-2705-4189-b628-095d995d0d33',
                            'Content-Type': 'text/xml'})

    attempts = 0
    while attempts < 3:
        try:

            # Check connection to Lightspeed server
            test_connection = session.get(current_store['address'])

            # Verify good response
            test_connection.raise_for_status()

            # Do work, bitch
            process_summary_records(current_store, session)
            process_detailed_records(current_store, session)

        except Exception as e:

            # log exception
            logging.error('Failed to connect to %s store. Exception: %s' % (current_store['store'], str(e)))

            # increase attempt counter
            attempts += 1

            # Log store connection attempt failure
            if attempts == 3:
                logging.info('%s | Store failure.' % current_store['store'])

            continue

        else:
            logging.info('%s | Store completed.' % current_store['store'])

            # Close API session gracefully
            session.close()

            # Break out of while loop check if no exception raised for status
            break


def process_summary_records(current_store, session):

    # types of records processed in this method
    document_types = ['customers', 'users', 'suppliers', 'products']

    # Loop through each document type
    for document_type in document_types:

        attempts = 0
        while attempts < 3:
            try:

                # Grab highest ID of uploaded document type
                lower_bound = current_store[document_type]

                # pull all records at products or users level
                if lower_bound is None or document_type == 'products' or document_type == 'users':
                    lower_bound = 0

                # grab following documents from last uploaded
                document_filter = {'filter': 'id > \"%s\"' % lower_bound}

                # Make API call with session parameters and method URL
                response = session.get(current_store['address'] + document_type + '/', params=document_filter)

                # Verify good response
                response.raise_for_status()

                # Create ET object for manipulation
                root = ElementTree.fromstring(response.text)

                # Break if there are no records of this type to pull
                if len(root.getchildren()) == 0:
                    logging.info('%s | Completed: No %s records to process.' % (current_store['storecode'],
                                                                                document_type))

                    # Break out of while attempt
                    break

                # Specify number of records being processed
                logging.info('%s | Processing: %d %s records.' % (current_store['storecode'], len(root.getchildren()),
                                                                  document_type))

                # Format data to be inserted into staging table
                insert_values = [(current_store['storecode'], root.tag, ElementTree.tostring(root))]

                # Do the insert
                db_client.insert_xml(insert_values)

            except Exception as e:

                # log exception
                logging.error('Failed to process %s data. Exception: %s' % (document_type, str(e)))

                # increase attempt counter
                attempts += 1

                continue

            else:

                logging.info('%s | Completed: %s data.' % (current_store['storecode'], document_type))

                # break out of while loop if no exceptions thrown
                break


def process_detailed_records(current_store, session):

    # types of records processed in this method
    document_types = ['purchase_order', 'invoice']

    # Loop through each document type
    for document_type in document_types:

        attempts = 0
        while attempts < 3:
            try:

                while True:

                    # Set default starting point for filter
                    lower_bound = current_store[document_type]

                    # Update lower_bound if there are records
                    if lower_bound is None:
                        lower_bound = 0

                    # Grab subset of records
                    document_filter = {'filter': 'id > \"%s\" AND id <= \"%s\"' % (lower_bound,
                                                                                   lower_bound + 500)}

                    # Make API call with session parameters and method URL/filter
                    response = session.get(current_store['address'] + document_type + 's/', params=document_filter)

                    # Create ET object for manipulation
                    root = ElementTree.fromstring(response.text)

                    # list that holds list of other documents to pull
                    document_list = []

                    # add uri's to list
                    for child in root:
                        document_list.append(child.get('uri'))

                    # Pull out of loop when no more records of this type to pull
                    if len(document_list) == 0:
                        break

                    # List to hold data to insert
                    insert_values = []

                    # Specify number of records being processed
                    logging.info(
                        '%s | Processing: %d %s records.' % (current_store['storecode'], len(root.getchildren()),
                                                             document_type))
                    # Loop through list of uri's and call each one
                    for document_uri in document_list:
                        response = session.get(document_uri)

                        root = ElementTree.fromstring(response.text)

                        insert_values.append((current_store['storecode'], root.tag, ElementTree.tostring(root)))

                    # Do insert
                    db_client.insert_xml(insert_values)

                    # Update store data
                    current_store = db_client.update_store(current_store['storecode'])

                break

            except Exception as e:

                # log exception
                logging.error('Failed to process %s data. Exception: %s' % (document_type, str(e)))

                # increase attempt counter
                attempts += 1

                continue

        logging.info('%s | Completed: %s data.' % (current_store['storecode'], document_type))

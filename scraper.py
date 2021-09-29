
import logging
import importlib

# councils = ['breakoday', 'brighton', 'burnie', 'centralcoast', 'centralhighlands', 'circularhead', 'clarence',
#             'derwentvalley', 'dorset', 'flinders', 'georgetown', 'glamorganspringbay', 'glenorchy', 'kentish',
#             'kingborough', 'kingisland', 'latrobe', 'meander', 'northernmidlands', 'tasman', 'waratahwynyard',
#             'westcoast', 'westtamar']

councils = ['breakoday', 'brighton']

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    records = []
    for council in councils:
        logging.debug(council)
        parser = importlib.import_module(council)
        newrecords = parser.councildas()
        for record in newrecords:
            record['authority_label'] = council
        records = records + newrecords
    for record in records:
        logging.debug(record)

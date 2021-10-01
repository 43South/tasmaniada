#!/usr/bin/env python3

import logging
import importlib
import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
import scraperwiki

councils = ['breakoday', 'brighton', 'burnie', 'centralcoast', 'centralhighlands', 'circularhead',
            # 'clarence',
            # 'derwentvalley',
            'dorset', 'flinders', 'georgetown', 'glamorganspringbay', 'glenorchy', 'kentish',
            'kingborough', 'kingisland', 'latrobe', 'meander', 'northernmidlands', 'tasman', 'waratahwynyard',
            'westcoast', 'westtamar']

# councils = ['breakoday', 'brighton']

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('starting')
    records = []
    for council in councils:
        parser = importlib.import_module(council)
        try:
            newrecords = parser.councildas()
            logging.info(f'{council}: found {len(newrecords)} applications')
            for record in newrecords:
                record['authority_label'] = council
            records = records + newrecords
        except Exception as e:
            logging.error(f'failed to run for {council}')
    for record in records:
        logging.debug(record)
        scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name='data')
    logging.info('finished')
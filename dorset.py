import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

def councildas():
    applications_url = \
        'https://eservices.dorset.tas.gov.au/eservice/dialog/daEnquiry/currentlyAdvertised.do?function_id=521&nodeNum=12237'
    html = scraperwiki.scrape(applications_url)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page('h4', 'non_table_headers')
    records = []
    for da in das:
        # todo: add Australia to address (but put postcode last). Not urgent as they put TAS into it already
        address = da.text
        info_url = 'https://eservices.dorset.tas.gov.au' + da.find('a')['href']
        council_reference = da.find_next('span', text='Application No.').next_sibling.text
        description = da.find_next('span', text='Type of Work').next_sibling.text
        date_received = parse(da.find_next('span', text='Date Lodged').next_sibling.text).strftime('%Y-%m-%d')
        record = {
          'council_reference': council_reference,
          'address': address,
          'description': description,
          'info_url': info_url,
          'date_scraped': date_scraped,
          'date_received': date_received,
        }
        records = records + [record]
    return records

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
    records = councildas()
    for record in records:
        logging.debug(record)
        scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name='data')
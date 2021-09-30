import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

def councildas():
    applications_url = 'https://www.westcoast.tas.gov.au/public-and-environmental-health/planning/planning-applications'
    html = scraperwiki.scrape(applications_url)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page('div', 'card-listing__item--has-cta')
    records = []
    for da in das:
        title = da.find_next('div', 'card-listing__title').text
        if not da.find_next('div', 'card-listing__title').text.startswith('DA'):
            continue
        addressdescription = da.find_next('div', 'card-listing__content').find_next('p').text
        address, description = addressdescription.split(' - ', 1)
        council_reference = title
        address = address.strip() + ', Tasmania, Australia'
        info_url =  da.find_next('a')['href']
        record = {
          'council_reference': council_reference,
          'address': address,
          'description': description.strip(),
          'info_url': info_url,
          'date_scraped': date_scraped,
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
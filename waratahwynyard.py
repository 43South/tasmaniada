import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

def councildas():
    applications_url = 'https://www.warwyn.tas.gov.au/planning-and-development/advertised-permits/'
    html = scraperwiki.scrape(applications_url)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    # das = page.find('table')('tr')[1:]
    das = page.find('h2', string='Planning Applications').find_next('table')('tr', 'file')
    records = []
    for da in das:
        text = da.find('span').text.strip()
        council_reference = text.split('-')[0].strip()
        address = text.split('-', 1)[1].strip() + ', Tasmania, Australia'
        description = 'devvelopment'
        info_url =  da.find('a')['href']
        record = {
          'council_reference': council_reference,
          'address': address,
          'description': description,
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
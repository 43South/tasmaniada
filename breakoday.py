import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
import logging

APPLICATIONS_URL = 'https://www.bodc.tas.gov.au/council/advertised-development-applications/'

def councildas():
    html = scraperwiki.scrape(APPLICATIONS_URL)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page.find('table')('tr')[1:]
    records = []
    for da in das:
        lines = da('td')
        council_reference = lines[3].text.strip()
        address = lines[1].text + ', Tasmania, Australia'
        description = lines[0].text
        info_url = lines[3].find('a')['href']
        on_notice_to = datetime.strptime(lines[2].text, '%d %B %Y').strftime('%Y-%m-%d')
        record = {
          'council_reference': council_reference,
          'address': address,
          'description': description,
          'info_url': info_url,
          'date_scraped': date_scraped,
          'date_received': None,
          'on_notice_from': None,
          'on_notice_to': on_notice_to
        }
        records = records + [record]
    return records

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
    records = councildas()
    for record in records:
        logging.debug(record)
        # scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name='data')


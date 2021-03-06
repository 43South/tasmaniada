import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse, ParserError
import logging

# This all feels horribly fragile. Smallest council = most work

def councildas():
    applications_url = 'https://centralhighlands.tas.gov.au/development-applications/'
    html = scraperwiki.scrape(applications_url)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page.find('div', 'twelve columns')
    locations = das(text='Location:')
    records = []
    for location in locations:
        addresselement = location.parent.next_sibling
        address = addresselement.rstrip().rstrip('/').strip() + ', Tasmania, Australia'
        info_url = addresselement.previous_sibling.find_next('a')['href']
        council_reference, description = location.find_next(text='Proposal:').parent.next_sibling.split('–', 2)
        paras = location.parent.find_all_next('p')
        if paras:
            for para in paras:
                if para.text.startswith('The relevant documents'):
                    on_notice_to = parse(' '.join(para.text.split()[-3:])).strftime('%Y-%m-%d')
                    break
        record = {
          'council_reference': council_reference.strip(),
          'address': address,
          'description': description.strip(),
          'info_url': info_url,
          'date_scraped': date_scraped,
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
        scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name='data')
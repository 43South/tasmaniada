import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

# TODO: PLN21-0231 was missed

def councildas():
    applications_url = 'https://www.northernmidlands.tas.gov.au/planning/development-in-the-northern-midlands/development-applications'
    html = scraperwiki.scrape(applications_url)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    # logging.debug(page.find('div', id='current-development-applications'))
    das = page.find('div', id='current-development-applications')('a')
    records = []
    for da in das:
        if not da.text.startswith('PLN-'):
            continue
        text = da.text
        council_reference = text.split()[0]
        address = text.split(' ', 2)[2].split(':')[0] + ', Tasmania, Australia'
        description = text.split(' ', 2)[2].split(':')[1].split('-')[1].strip()
        info_url =  'https://www.northernmidlands.tas.gov.au/' + da['href']
        on_notice_to = parse(da.find_previous('h2').text.split(' ', 1)[1]).strftime('%Y-%m-%d')
        record = {
          'council_reference': council_reference,
          'address': address,
          'description': description,
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
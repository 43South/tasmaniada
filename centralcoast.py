import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse, ParserError
import logging

logging.basicConfig(level=logging.DEBUG)

def councildas():
    applications_url = 'https://www.centralcoast.tas.gov.au/current-planning-applications'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    html = scraperwiki.scrape(applications_url, user_agent=user_agent)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page.find_all('div', 'listing-item')
    expiryprefixlen = len('Notification expiry date - ')
    records = []
    for da in das:
        descriptionraw, expiryraw = da.find('span', 'excerpt').text.split(')')
        description = descriptionraw.split('(')[0].strip()
        on_notice_to = parse(expiryraw.split('[')[1][expiryprefixlen:-1]).strftime('%Y-%m-%d')
        council_reference, dummy, address = da.find('a').text.split(' ', 2)
        address = address + ', Tasmania, Australia'
        info_url = da.find('a')['href']
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
        # scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name='data')
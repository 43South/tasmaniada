import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse, ParserError
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://gsbc.tas.gov.au/services-facilities/public-notices/'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')

das = page.find('strong', string='APPLICATIONS FOR PLANNING PERMITS').find_all_next('tr')
for da in das:
    column = da('td')
    # ignore the heading row
    if len(column) == 0:
        continue
    description = column[0].get_text().strip()
    address, council_reference = column[1].get_text().strip().rsplit(' ', 1)
    date_received = parse(column[2].get_text()).strftime('%Y-%m-%d')
    on_notice_to = parse(column[3].get_text()).strftime('%Y-%m-%d')
    info_url = column[4].find('a')['href']
    record = {
      'council_reference': council_reference,
      'address': address + ', Tasmania, Australia',
      'description': description,
      'info_url': info_url,
      'date_scraped': date_scraped,
      'date_received': date_received,
      'on_notice_to': on_notice_to
    }
    logging.debug(record)
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

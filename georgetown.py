import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse, ParserError
import logging
import re

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://georgetown.tas.gov.au/current-development-applications'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')

das = page('strong', string='PROPOSAL')
for da in das:
    description = da.next_sibling
    address = da.parent.next_sibling
    address, council_reference = da.find_next('strong', string=re.compile('LOCATION')).next_sibling.rsplit('(', 1)
    info_url = 'https://georgetown.tas.gov.au/' + da.find_next('a')['href']
    on_notice_to = parse(da.find_next('strong', string=re.compile('CLOSES')).next_sibling.strip()).strftime('%Y-%m-%d')
    record = {
      'council_reference': council_reference.rstrip(')'),
      'address': address.replace('\xa0', '').strip() + ', Tasmania, Australia',
      'description': description.strip().replace('\xa0', ''),
      'info_url': info_url,
      'date_scraped': date_scraped,
      'on_notice_to': on_notice_to
    }
    logging.debug(record)
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

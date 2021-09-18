

import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse, ParserError
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.devonport.tas.gov.au/building-development/planning/advertised-planning-permit-applications/'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')

das = page.find('table')('tr', 'file')
# print(das)

for da in das:
    element = da.find('a')
    council_reference, address, description, rawdate = element.get_text().split('-')
    on_notice_to = parse(' '.join(rawdate.split()[-3:])).strftime('%Y-%m-%d')
    info_url = element['href']
    record = {
      'council_reference': council_reference.strip(),
      'address': address.strip() + ', Tasmania, Australia',
      'description': description.strip(),
      'info_url': info_url,
      'date_scraped': date_scraped,
      'on_notice_to': on_notice_to
    }
    logging.debug(record)
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

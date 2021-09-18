import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.kentish.tas.gov.au/services/building-and-planning-services/planningapp'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')
das = page.find(string='Current Planning Applications').find_all_next('ul')[0]('li')
for da in das:
    aelement = da.find_next('a')
    text = aelement.get_text()
    bits = text.split()
    council_reference = ' '.join(bits[0:2])
    # sometimes there's no description, so I dummy one in then take it out if it's not needed
    address, description = (' '.join(bits[2: -7]).strip() + '-').split('-', 1)
    description = description.rstrip('-').strip()
    info_url =  aelement['href']
    on_notice_to = parse(text.rsplit('(', 2)[1][15:-2]).strftime('%Y-%m-%d')
    record = {
      'council_reference': council_reference,
      'address': address.strip() + ', Tasmania, Australia',
      'description': description,
      'info_url': info_url,
      'date_scraped': date_scraped,
      'on_notice_to': on_notice_to
    }
    logging.debug(record)
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

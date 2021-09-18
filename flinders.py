import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.flinders.tas.gov.au/current-advertising'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')
das = page.find('div', id='docList')('h2')
for da in das:
    council_reference, address, dummy = da.find_previous('h1').get_text().split('-')
    description = da.get_text()
    info_url = 'https://www.flinders.tas.gov.au/' + da.find_all_next('li')[1].find('a')['href']
    record = {
      'council_reference': council_reference.strip(),
      'address': address.strip() + ', Tasmania, Australia',
      'description': description,
      'info_url': info_url,
      'date_scraped': date_scraped,
    }
    logging.debug(record)
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

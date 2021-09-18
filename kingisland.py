import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://kingisland.tas.gov.au/develop/planning/'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')
das = page.find('div', 'devapps')('a', 'ccpage_title_link')
for da in das:
    logging.debug(da)
    council_reference = ''
    refaddress, description = da.get_text().rsplit('–', 1)
    bits = refaddress.split()
    council_reference = ' '.join(bits[0:2])
    address = ' '.join(bits[2:]) + ', Tasmania, Australia'
    info_url =  da['href']
    record = {
      'council_reference': council_reference,
      'address': address,
      'description': description.strip(),
      'info_url': info_url,
      'date_scraped': date_scraped,
    }
    logging.debug(record)
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

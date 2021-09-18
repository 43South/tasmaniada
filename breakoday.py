import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
import logging


logging.basicConfig(level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.bodc.tas.gov.au/council/advertised-development-applications/'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')

das = page.find('table')('tr')[1:]
for da in das:
    lines = da('td')
    council_reference = lines[3].get_text().strip()
    address = lines[1].get_text() + ', Tasmania, Australia'
    description = lines[0].get_text()
    info_url = lines[3].find('a')['href']
    on_notice_to = datetime.strptime(lines[2].get_text(), '%d %B %Y').strftime('%Y-%m-%d')
    record = {
      'council_reference': council_reference,
      'address': address,
      'description': description,
      'info_url': info_url,
      'date_scraped': date_scraped,
      'on_notice_to': on_notice_to
    }
    logging.debug(record)
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

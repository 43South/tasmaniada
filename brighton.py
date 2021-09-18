import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse, ParserError
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.brighton.tas.gov.au/planning/advertised-development-applications/'
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
    try:
        on_notice_to = parse(lines[2].get_text()).strftime('%Y-%m-%d')
    except ParserError:
        on_notice_to = ''
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

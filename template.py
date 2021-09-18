import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')
das = page.find('table')('tr')[1:]
for da in das:
    council_reference = ''
    address = '' + ', Tasmania, Australia'
    description = ''
    info_url =  '' #  .('a')['href']
    on_notice_to = parse('1 jan 2020').strftime('%Y-%m-%d')
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

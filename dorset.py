import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = \
    'https://eservices.dorset.tas.gov.au/eservice/dialog/daEnquiry/currentlyAdvertised.do?function_id=521&nodeNum=12237'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')
das = page('h4', 'non_table_headers')
for da in das:
    address = da.get_text()
    info_url = 'https://eservices.dorset.tas.gov.au' + da.find('a')['href']
    council_reference = da.find_next('span', text='Application No.').next_sibling.get_text()
    description = da.find_next('span', text='Type of Work').next_sibling.get_text()
    date_received = parse(da.find_next('span', text='Date Lodged').next_sibling.get_text()).strftime('%Y-%m-%d')
    record = {
      'council_reference': council_reference,
      'address': address,
      'description': description,
      'info_url': info_url,
      'date_scraped': date_scraped,
      'date_received': date_received,
    }
    logging.debug(record)
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

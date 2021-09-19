import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.meander.tas.gov.au/advertised-approved-planning-applications'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')
das = page('strong', string='Applicant: ')
for da in das:
    datr = da.find_previous('tr')
    council_reference = datr.find('a').get_text()
    lines = datr.find_next('strong', string='Address: ').parent.prettify().splitlines()
    address = lines[19].rsplit('(', 2)[0].strip() + ', Tasmania, Australia'
    description = lines[24].strip()
    info_url =  'https://www.meander.tas.gov.au/' + datr.find('a')['href']
    on_notice_to = parse(lines[-2]).strftime('%Y-%m-%d')
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

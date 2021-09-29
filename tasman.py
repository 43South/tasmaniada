import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.tasman.tas.gov.au/developmentservices/publicnotices/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
html = scraperwiki.scrape(applications_url, user_agent=user_agent)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')
das = page('div', class_='filetitle')
for da in das:
    text = da.find('a').text
    logging.debug(text)
    council_reference = ' '.join(text.split(' ', 2)[0:2]).strip()
    address = text.split(' ', 2)[2].rsplit('(')[0].lstrip(' -').rstrip() + ', Tasmania, Australia'
    description = 'development'
    info_url =  da.find('a')['href']
    on_notice_to = parse(' '.join(text.rsplit(' ', 4)[2:])).strftime('%Y-%m-%d')
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
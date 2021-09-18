import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse, ParserError
import logging

logging.basicConfig(level=logging.DEBUG)


os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.burnie.net/Development/Planning/Permit-applications-on-exhibition'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')
das = page.find_all('article')
ondisplayprefix = len('On display until ') + 2
for da in das:
    lines = da.get_text().splitlines()
    council_reference = da.find('p', 'da-application-number').get_text()
    description = da('p')[-1].get_text()
    info_url = da.find('a')['href']
    address = da.find('p', 'list-item-address').get_text() + ', Tasmania, Australia'
    on_notice_to = parse(da.find('p', 'display-until-date').get_text()[ondisplayprefix:]).strftime('%Y-%m-%d')
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

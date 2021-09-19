import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime


def getfield(lines_, key):
    return [line.split(':', 1)[1] for line in lines if line.split(':')[0] == key][0].strip()


os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.gcc.tas.gov.au/services/planning-and-building/planning-and-development/planning-applications/'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')

das = page.find_all('div', 'content-block__inner')
# print(das)
for da in das:
    refandaddress = da.find('a').get_text().strip()
    council_reference, dummy, address = refandaddress.split(' ', 2)
    address = address + ', Tasmania, Australia'
    info_url = da('a')[1]['href']
    # print(da)
    description = da.find('div', 'content-block__description').get_text().strip()
    rawcloses = da.find('p', 'content-block__date').get_text().split(':')[1].strip()
    on_notice_to = datetime.strptime(rawcloses, '%d %B %Y').strftime('%Y-%m-%d')
    record = {
      'council_reference': council_reference,
      'address': address,
      'description': description,
      'info_url': info_url,
      'date_scraped': date_scraped,
      'on_notice_to': on_notice_to
    }
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

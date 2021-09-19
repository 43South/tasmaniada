import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime


def getfield(lines_, key):
    return [line.split(':', 1)[1] for line in lines if line.split(':')[0] == key][0].strip()


os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
applications_url = 'https://www.wtc.tas.gov.au/Your-Property/Planning/Currently-Advertised-Planning-Applications'
html = scraperwiki.scrape(applications_url)
date_scraped = datetime.now().isoformat()
page = BeautifulSoup(html, 'html.parser')
das = page.find_all('article')
for da in das:
    lines = da.get_text().splitlines()
    council_reference = das[0].find('h2').get_text().split(':')[1].strip()
    info_url = das[0].find('a')['href']
    address = getfield(lines, 'LOCATION') + ', Tasmania, Australia'
    description = getfield(lines, 'PROPOSAL')
    # they use both : and . as hour:minute separator
    rawcloses = getfield(lines, 'CLOSES').replace(':', '.')
    on_notice_to = datetime.strptime(rawcloses, '%I.%M%p %d %B %Y').strftime('%Y-%m-%d')
    record = {
      'council_reference': council_reference,
      'address': address,
      'description': description,
      'info_url': info_url,
      'date_scraped': date_scraped,
      'on_notice_to': on_notice_to
    }
    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")

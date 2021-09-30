import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import ssl

def getfield(lines_, key):
    return [line.split(':', 1)[1] for line in lines_ if line.split(':')[0] == key][0].strip()

def councildas():
    # it's never easy
    ssl._create_default_https_context = ssl._create_unverified_context
    applications_url = 'https://www.wtc.tas.gov.au/Your-Property/Planning/Currently-Advertised-Planning-Applications'
    html = scraperwiki.scrape(applications_url)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page.find_all('article')
    records = []
    for da in das:
        lines = da.text.splitlines()
        heading = da.find('h2').text
        # the planning scheme ammendment is in a different format
        if not heading.startswith('PA NO'):
            continue
        council_reference = heading.split(':')[1].strip()
        info_url = da.find('a')['href']
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
        records = records + [record]
    return records

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
    records = councildas()
    for record in records:
        logging.debug(record)
        scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name='data')
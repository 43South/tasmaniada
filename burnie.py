import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse, ParserError
import logging

def councildas():
    applications_url = 'https://www.burnie.net/Development/Planning/Permit-applications-on-exhibition'
    html = scraperwiki.scrape(applications_url)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page.find_all('article')
    ondisplayprefix = len('On display until ') + 2
    records = []
    for da in das:
        lines = da.text.splitlines()
        council_reference = da.find('p', 'da-application-number').text
        description = da('p')[-1].text
        info_url = da.find('a')['href']
        address = da.find('p', 'list-item-address').text + ', Tasmania, Australia'
        on_notice_to = parse(da.find('p', 'display-until-date').text[ondisplayprefix:]).strftime('%Y-%m-%d')
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
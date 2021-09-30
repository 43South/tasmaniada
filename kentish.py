import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging
import urllib.error

def councildas():
    applications_url = 'https://www.kentish.tas.gov.au/services/building-and-planning-services/planningapp'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    # This may be unnecessary, but I kept getting HTTPGone
    for tries in range(0, 5):
        try:
            html = scraperwiki.scrape(applications_url, user_agent=user_agent)
            break
        # except urllib.error.HTTPError as e:
        except Exception as e:
            logging.error(e)
    else:
        return []
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page.find(string='Current Planning Applications').find_all_next('ul')[0]('li')
    records = []
    for da in das:
        aelement = da.find_next('a')
        text = aelement.text
        bits = text.split()
        council_reference = ' '.join(bits[0:2])
        # sometimes there's no description, so I dummy one in then take it out if it's not needed
        address, description = (' '.join(bits[2: -7]).strip() + '-').split('-', 1)
        description = description.rstrip('-').strip()
        info_url =  aelement['href']
        on_notice_to = parse(text.rsplit('(', 2)[1][15:-2]).strftime('%Y-%m-%d')
        record = {
          'council_reference': council_reference,
          'address': address.strip() + ', Tasmania, Australia',
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
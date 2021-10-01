import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
import logging

# This is horribly fragile

# TODO: scraper failing sometimes. Unknown cause


def councildas():
    applications_url = 'https://www.circularhead.tas.gov.au/council-services/development/planning'
    html = scraperwiki.scrape(applications_url)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page.find(text='Current Planning Permit Applications').find_all_next('li')
    records = []
    for da in das:
        info_url = da.find('a')['href']
        refaddressdesc = da.find('a').text
        # this is so horrible I can hardly make myself do it
        bits = refaddressdesc.split('-')
        if not bits[1] == '2021':
            if bits[0].endswith('2021'):
                bits = [bits[0][0:2], bits[0][2:]] + bits[1:]
            else:
                # impossible, skip this one
                continue
        council_reference = '-'.join(bits[0:3])
        address = ' '.join(bits[3: 6]) + ', ' + bits[6] + ', Tasmania, Australia'
        description = ' '.join(bits[7:-1] + [bits[-1].split('.')[0]])
        record = {
          'council_reference': council_reference,
          'address': address,
          'description': description,
          'info_url': info_url,
          'date_scraped': date_scraped,
        }
        records = records + [record]
    return records


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
    records = councildas()
    for record in records:
        logging.debug(record)
        # scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name='data')

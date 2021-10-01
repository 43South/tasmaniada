import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

def councildas():
    applications_url = 'https://www.tasman.tas.gov.au/developmentservices/publicnotices/'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
    html = scraperwiki.scrape(applications_url, user_agent=user_agent)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    das = page('div', class_='filetitle')
    records = []
    for da in das:
        text = da.find('a').text
        # TODO: one case of double reference, 'SA 05-2012-75 & 51' Tricky to parse
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
        records = records + [record]
    return records

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
    records = councildas()
    for record in records:
        logging.debug(record)
        scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name='data')
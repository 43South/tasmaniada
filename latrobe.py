import os
import scraperwiki
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import logging

# TODO: failed to run. Gets HTTPGone sometimes. Maybe it's too fast. Retry?

def councildas():
    applications_url = 'https://www.latrobe.tas.gov.au/services/building-and-planning-services/planningapp'
    html = scraperwiki.scrape(applications_url)
    date_scraped = datetime.now().isoformat()
    page = BeautifulSoup(html, 'html.parser')
    # das = page.find('table')('tr')[1:]
    das = page.find(string='CURRENT PLANNING APPLICATIONS').find_all_next('ul')[0]('li')
    records = []
    for da in das:
        # formatting of entries varies considerable
        # DA 158-2021 1055 Port Sorell Road, Northdown - proposed Subdivision and Consolidation (submissions by 4.40 29/9/2021) (PDF File, 5.3 MB)
        # DA 184/2021 - 59 Hamilton Street, Latrobe - proposed Demolition of Existing Dwelling and Proposed Development of Multiple Dwellings (4 Units) - submissions by 4.40pm 29/9/2021 (PDF File, 7.9 MB)
        aelement = da.find_next('a')
        text = aelement.text
        bits = text.split()
        council_reference = ' '.join(bits[0:2])
        proppos = text.find('proposed')
        refaddress = text[0:proppos].rstrip(' -').split(' ', 2)
        council_reference = ' '.join(refaddress[0:2])
        address = refaddress[2].lstrip(' -')
        description = text[proppos:].rsplit('(', 2)[0].strip()
        info_url =  aelement['href']
        on_notice_to = parse(text.rsplit('(', 1)[0].rsplit(' ', 2)[1].strip(')')).strftime('%Y-%m-%d')
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
        # scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name='data')
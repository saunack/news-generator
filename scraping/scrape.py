from selenium import webdriver
import scrapy
import pandas as pd
import time
import sys
import logging
import daiquiri
import os

ROOT_DIR = 'raw_scrape'
START_YEAR = 2009
START_MONTH = 8
END_YEAR = 2020
END_MONTH = 8
filename = os.path.join(ROOT_DIR,str(START_YEAR))
CSV = filename + '.csv'
LOGFILE = filename + '.log'

# logger
daiquiri.setup(level=logging.INFO,outputs=(
    daiquiri.output.Stream(sys.stdout),
    daiquiri.output.File(LOGFILE,
                         formatter=daiquiri.formatter.JSON_FORMATTER),
    ))
logger = daiquiri.getLogger(__name__)

# options for webdriver (can add 'headless' too)
op = webdriver.ChromeOptions()
op.add_argument('incognito')
# create instance
archive = webdriver.Chrome(options=op)
article = webdriver.Chrome(options=op)

baseURL = 'https://www.thehindu.com/archive/web/'

titles = []
links = []
texts = []
years = []
months = []
dates = []
absent = []
count = 0

def add_editorials(url, titles = [], links = [], texts = []):
    archive.get(url)
    editorials = archive.find_elements_by_xpath('//h2[@id="editorial"]//ancestor::div[@class="section-header"]//following-sibling::div[@class="section-container"]//a')
    
    for e in editorials:
        link = e.get_attribute('href')
        article.get(link)
        # /p directly works as well, but jsut to be sure
        try:
            count += 1
            if count == 10:
                # need to reset browser to keep under the free 10 article/day limit
                article.quit()
                article = webdriver.Chrome(options=op)
                count = 0
            
            p_elems = article.find_elements_by_xpath('//div[contains(@id,"content-body-")]/p')
            paragraphs = [p.text for p in p_elems]
            texts.append('\n'.join(paragraphs))
            titles.append(e.text)
            links.append(link)
        except:
            logging.warning('TIMEOUT: link {} missed from {}'.format(link, url))

    return titles, links, texts

for year in range(START_YEAR,END_YEAR):
    for month in range(1,13):
        for date in range(1,32):
            
            if year == START_YEAR and month < START_MONTH:
                continue
            if year == END_YEAR and month > END_MONTH:
                continue
            if year == 2009 and month == 8 and date < 12:
                continue
            if month == 2 and date > 29:
                continue
            if month not in [1,3,5,7,8,10,12] and date > 30:
                continue
            
            url = baseURL + str(year) + '/' + str(month) + '/' + str(date)
            initial = len(texts)
            titles, links, texts = add_editorials(url, titles, links, texts)
            final = len(texts)
            for _ in range(final-initial):
                years.append(year)
                months.append(month)
                dates.append(date)
            if final == initial:
                logging.debug("MISSING {}/{}/{}".format(date, month, year))
                logging.warning("{}/{}/{} not present".format(date, month, year))
                time.sleep(10)

        logging.info("MONTH {}/{} finished".format(month, year))
        df = pd.DataFrame({'Date':dates,'Month':months,'Year':years,'Title':titles,'Content':texts,'Link':links})
        df.to_csv(CSV,index=False,encoding='utf-8')
    logging.info("YEAR {} finished".format(year))

logging.info("REACHED END")
data = {'Date':dates,'Month':months,'Year':years,'Title':titles,'Content':texts,'Link':links}
df = pd.DataFrame(data)
df.to_csv(CSV,index=False,encoding='utf-8')

archive.quit()
article.quit()

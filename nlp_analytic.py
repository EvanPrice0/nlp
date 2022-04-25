import mechanicalsoup
from urllib.request import urlopen
import requests
from datetime import date
import sys

base_url="https://www.imf.org/"
initial_search_query_preset="en/Publications/Search?series=&when=During&year="

def get_url(year,title):
    return base_url+initial_search_query_preset+year+"&title='"+title+"'"

def get_browser_soup(browser, url, query=None, atts=None):
    login_page = browser.get(url)
    soup = login_page.soup
    find=query or atts
    if(find==query):
        find_all=soup.find_all(query)
    else:
        find_all=soup.find_all(attrs=atts)
    return find_all


def cook_soup(queryatts,value, browser,base_url):
    new_url=[]
    if(queryatts==True):
        new_spot=get_browser_soup(browser, base_url, query=value)
    else:
        new_spot=get_browser_soup(browser, base_url, atts=value)
    for spots in new_spot:
        new_url.append("https://www.imf.org"+spots.get('href'))
    return new_url

if __name__ == "__main__":
    country=sys.argv[1]
    year=sys.argv[2]
    base_url=get_url(year,country)
    lambdafunction=lambda k:k.name=='a' and country in k.text
    browser = mechanicalsoup.Browser()
    attrs={'class':'piwik_download'}
    new_spot=cook_soup(True,lambdafunction,browser,base_url)
    newer_spot=[]
    for spots in new_spot:
        spot_here=cook_soup(False, value=attrs, browser=browser, base_url=spots)
        for ind_spot in spot_here:
            newer_spot.append(ind_spot)
    iter=0
    for spot in newer_spot:
        resp = requests.get(spot)
        now = date.today().isoformat()
        with open(country.replace(" ", "").lower()+'_'+now+'_'+str(iter)+'.xls', 'wb') as f:
            f.write(resp.content)
            iter+=1
            f.close()
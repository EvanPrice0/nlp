import mechanicalsoup
from bs4 import BeautifulSoup
from urllib.request import urlopen

url= "https://www.imf.org/en/Publications/Search?series=IMF%20Staff%20Country%20Reports&when=During&year=2022&title=Kenya"
browser = mechanicalsoup.Browser()
login_page = browser.get(url)
print(login_page.content)
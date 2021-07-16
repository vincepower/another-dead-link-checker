from bs4 import BeautifulSoup
from markdown import markdown
import requests
import urllib3
from urllib.parse import urlparse
import sys
from colorama import Fore,Style,Back,init

# Using init from \colorama so it works
init(autoreset=True)

# Checking if there is a URL passed, fail if not
try:
    arg = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <url_for_page_to_check>")

# Let's get the base domain so local links can be tested too
parsed_url = urlparse(arg)
base_url = parsed_url.scheme+"://"+parsed_url.netloc
url_path_parts = parsed_url.path.split("/")
for url_path_part in url_path_parts[:-1]:
    base_url = base_url+"/"+url_path_part

# Defining which parse to use for BeautifulSoup
parser = 'html.parser'

# Retriving the page to find the links on
http = urllib3.PoolManager()
resp = http.request('GET', arg)

# Letting BeautifulSoup do its thing
soup = BeautifulSoup(resp.data, parser)

# Looking through all the a[nchor] tags on the page
for link in soup.find_all('a', href=True):
    # If the link starts with http, https, or // just let it go
    # if it doesn't then add the base_url we figure out earlier
    if link['href'].startswith("http://"):
        tested = requests.get(link['href'], allow_redirects=False)
    elif link['href'].startswith("https://"):
        tested = requests.get(link['href'], allow_redirects=False)
    elif link['href'].startswith("//"):
        tested = requests.get("https:"+link['href'], allow_redirects=False)
    else:
        tested = requests.get(base_url+link['href'], allow_redirects=False)

    # Using colorama to make 2xx status codes green,
    # 3xx yellow, and the rest red
    if str(tested.status_code).startswith("2"):
        print(Fore.GREEN + Back.BLACK + tested.url + "\t" + str(tested.status_code))
    elif str(tested.status_code).startswith("3"):
        print(Fore.YELLOW + Back.BLACK + tested.url + "\t" + str(tested.status_code))
    else:
        print(Fore.RED + Back.BLACK + tested.url + "\t" + str(tested.status_code))

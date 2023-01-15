import requests
from bs4 import BeautifulSoup
import random

# the base URL of the website to crawl
base_url = "https://www.thrasio.com"

# create an empty set to store the visited URLs
visited_urls = set()

page_num = 0

def crawl(url):
    # send a request to the website and get the HTML response
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html = response.text

    # parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # create an empty list to store the relevant text
    text = []

    # find all the elements that contain text
    for element in soup.find_all(text=True):
        # ignore buttons, links, and forms
        if element.parent.name in ['button', 'a', 'form']:
            continue

        # only keep the text if it is in a sentence
        if element.strip().endswith(('.', '?', '!')):
            text.append(element.strip())

    # format the text as specified
    formatted_text = "------------------------\n"
    formatted_text += url + "\n"
    formatted_text += "------------------------\n"
    formatted_text += '\n'.join(text) + "\n\n"

    return formatted_text


def get_all_urls(url):
    global page_num
    
    # send a request to the website and get the HTML response
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html = response.text

    # parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    html_text = soup.prettify()

    # save the HTML text to a .html file
    # random
    page_num = page_num + 1
    with open(f'pages/{page_num}.html', 'w') as f:
        f.write(html_text)

    # find all the links on the page
    links = soup.find_all('a')

    # add the URL to the set of visited URLs
    visited_urls.add(url)

    # create an empty list to store the sub-URLs
    sub_urls = []

    # iterate through the links and get the sub-URLs
    for link in links:
        href = link.get('href')
        if href and href.startswith(base_url) and href not in visited_urls:
            sub_urls.append(href)

    return sub_urls

# start the crawl at the base URL
urls_to_visit = [base_url]

# create an empty string to store the formatted text
formatted_text = ""

while len(urls_to_visit) > 0 and len(visited_urls) < 1000:
    # get the next URL to visit
    url = urls_to_visit.pop(0)

    # crawl the URL and get the formatted text
    text = crawl(url)
    formatted_text += text

    # get the sub-URLs of the current URL
    sub_urls = get_all_urls(url)

    # add the sub-URLs to the list of URLs to visit
    urls_to_visit.extend(sub_urls)

    # save the formatted text to a .txt file
    with open('text.txt', 'w') as f:
        f.write(formatted_text + '\n')



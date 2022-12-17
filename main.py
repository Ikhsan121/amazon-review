import pandas as pd
import requests
from bs4 import BeautifulSoup

search_query = "nike+shoes+men"
base_url = 'https://www.amazon.com/s?k='
url = base_url+search_query

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'referer': 'https://www.amazon.com/s?k=nike+shoes+men&language=en_US&crid=7T3NTJ4XDMVF&currency=IDR&sprefix=nike%2Caps%2C577&ref=nb_sb_ss_ts-doa-p_3_4s',
}

search_response = requests.get(url, headers=header)

cookie = search_response.cookies


def getAmazonSearch(search_query):
    url = 'https://www.amazon.com/s?k='+search_query
    # print(url)
    page = requests.get(url, headers=header, cookies=cookie)
    if page.status_code == 200:
        return page
    else:
        return "error"


# Function to get the contents of individual product pages using 'data-asin' number (unique identification number)
def Searchasin(asin):
    url = 'https://www.amazon.com/dp/'+asin
    # print(url)
    page = requests.get(url, cookies=cookie, headers=header)
    if page.status_code == 200:
        return page
    else:
        return "error"


# Function to pass on the link of 'see all reviews' and extract the content
def Searchreviews(review_link):
    url= 'https://www.amazon.com'+review_link
    # print(url)
    page = requests.get(url, cookies=cookie, headers=header)
    if page.status_code == 200:
        return page
    else:
        return "error"

# First page product reviews extraction
product_names = []
response = getAmazonSearch('nike+shoes+men')
soup = BeautifulSoup(response.content, 'html.parser')
for i in soup.find_all("span", {'class': 'a-size-base-plus a-color-base a-text-normal'}):
    product_names.append(i.text) # adding product name to the list

print(len(product_names))


# The method of extracting data-asin numbers are similar to that of product names, Only the tag details have to be change in find_alL()
data_asin = []
response = getAmazonSearch('nike+shoes+men')
soup = BeautifulSoup(response.content, 'html.parser')
for i in soup.find_all('div', {'class': 'sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'}):
    data_asin.append(i['data-asin'])

print(len(data_asin))

# By passing the data-asin numbers, we can extract the 'see all reviews' link for each product in the stage
link = []
for i in range(len(data_asin)):
    response = Searchasin(data_asin[i])
    soup = BeautifulSoup(response.content, 'html.parser')
    for i in soup.find_all('a', {'data-hook': 'see-all-reviews-link-foot'}):
        link.append(i['href'])

reviews = []
for j in range(len(link)):
    for k in range(3):
        response = Searchreviews(link[j]+'&pageNumber='+str(k))
        soup = BeautifulSoup(response.content, 'html.parser')
        for i in soup.find_all('span', {'data-hook': 'review-body'}):
            reviews.append(i.text)
        print('k is scraped: ', k)

rev = {'reviews': reviews}
review_data = pd.DataFrame.from_dict(rev)
pd.set_option('max_colwidth', 800)

review_data.to_csv('scraping review.csv', index=False)
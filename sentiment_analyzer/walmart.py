import re
import csv
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import request

walmart_laptop_url = 'https://www.walmart.com/search/?cat_id=0&query=laptop'
walmart_mobile_url = 'https://www.walmart.com/browse/cell-phones/1105910?facet=brand%3ASamsung&grid=false&page=1#searchProductResult'
amazon_url = 'https://www.amazon.com/s?k='
flipkart_url = 'https://www.flipkart.com/search?q='


class WalmartProduct:

    def __init__(self, title='', link='', rating='', price='', image='', alt_tag='', search_term=''):
        self.title = title
        self.walmart_link = link
        self.walmart_rating = rating
        self.walmart_price = price
        self.image = image
        self.alt_tag = alt_tag
        self.search_term = search_term


class Amazon(WalmartProduct):
    amazon_price = ''
    amazon_rating = ''
    amazon_title = ''
    amazon_link = ''
    amazon_voted = ''


class Flipkart(WalmartProduct):
    flipkart_link = ''
    flipkart_price = ''
    flipkart_rating = ''
    flipkart_voted = ''


def parsing_html_page(url):
    page_source = request.urlopen(url)
    soup = BeautifulSoup(page_source, 'lxml')
    return soup


def csv_conversion(obj, filename, identity):
    # initialize Regular Expression object
    w_ratingRegex = re.compile(r'\d\.?\d*')
    a_ratingRegex = re.compile(r'\d\.\d+')
    f_ratingRegex = re.compile(r'\d+')
    if identity == 'laptop':
        laptop_fields = ['Title', 'Image', 'Walmart Price', 'Walmart Rating', 'Walmart Voted', 'Walmart Link',
                         'Amazon Price', 'Amazon Rating', 'Amazon Voted', 'Amazon Link']

        laptop_file_name = filename

        with open(laptop_file_name, 'w') as laptop_csv_file:

            # creating csv writer object
            laptop_csv_writer = csv.writer(laptop_csv_file)

            # writing the fields 
            laptop_csv_writer.writerow(laptop_fields)

            # writing the data rows

            for l_data in obj:
                try:
                    w_list = w_ratingRegex.findall(l_data.walmart_rating)
                    w_rating = w_list[0]
                    w_voted = w_list[2]
                except:
                    w_rating = ''
                    w_voted = ''
                try:
                    a_rating = a_ratingRegex.findall(l_data.amazon_rating)[0]
                except:
                    a_rating = ''
                laptop_csv_writer.writerow(
                    [l_data.title, l_data.image, l_data.walmart_price, w_rating, w_voted, l_data.walmart_link,
                     l_data.amazon_price, a_rating, l_data.amazon_voted, l_data.amazon_link])

    elif (identity == 'mobile'):
        mobile_fields = ['Title', 'Image', 'Walmart Price', 'Walmart Rating', 'Walmart Voted', 'Walmart Link',
                         'Flipkart Price', 'Flipkart Rating', 'Flipkart Link', 'Flipkart voted']
        mobile_file_name = filename
        with open(mobile_file_name, 'w') as mobile_csv_file:
            mobile_csv_writer = csv.writer(mobile_csv_file)
            mobile_csv_writer.writerow(mobile_fields)
            for m_data in obj:
                try:
                    w_list = w_ratingRegex.findall(m_data.walmart_rating)
                    w_rating = w_list[0]
                    w_voted = w_list[2]
                except:
                    w_rating = ''
                    w_voted = ''
                try:
                    f_voted = f_ratingRegex.findall(m_data.flipkart_rating)
                    f_voted = ''.join(f_voted)
                except:
                    f_voted = ''

                mobile_csv_writer.writerow(
                    [m_data.title, m_data.image, m_data.walmart_price, w_rating, w_voted, m_data.walmart_link,
                     m_data.flipkart_price, m_data.flipkart_rating, m_data.flipkart_link, f_voted])


def collect_data_from_walmart(url, identity):
    soup = parsing_html_page(url)
    products = soup.find_all(class_='search-result-listview-item Grid')

    walmart_product = []

    for product in products:

        title = product.find('a', class_='product-title-link line-clamp line-clamp-2')['title']
        link = 'https://www.walmart.com' + product.find('a', class_='product-title-link line-clamp line-clamp-2')[
            'href']
        try:
            rating = product.find('span', class_='stars-container')['alt']
        except:
            rating = ''
        try:
            price = product.find('span', class_='price display-inline-block arrange-fit price price-main').span[
                'aria-label']
        except:
            price = ''
        img = product.img
        image = img['data-image-src']
        alt_tag = img['alt']

        # making search term compatible for amazon
        search_term = alt_tag.split(',')[0].split(' ')
        search_term = '+'.join(search_term)

        # initializing walmart an object
        if (identity == 'laptop'):
            walmart_obj = Amazon(title, link, rating, price, image, alt_tag, search_term)
        elif (identity == 'mobile'):
            walmart_obj = Flipkart(title, link, rating, price, image, alt_tag, search_term)

        walmart_product.append(walmart_obj)

    return walmart_product


# collecting data from amazon
def collect_data_from_amzn(walmart_product):
    driver = webdriver.PhantomJS(executable_path='D:\installed\phantomjs.exe')
    for p in walmart_product:

        print("searching Now: " + p.search_term)
        url = amazon_url + p.search_term + "&s=review-rank"

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        products = soup.find_all('div',
                                 class_='sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28')[
                   :1]

        for product in products:
            try:
                p.amazon_price = product.find('span', class_='a-offscreen').string
            except:
                p.amazon_price = ''
            try:
                p.amazon_rating = product.find('div', class_='a-row a-size-small').span['aria-label']
            except:
                p.amazon_rating = ''
            try:
                amazon_voted = product.find('div', class_='a-row a-size-small')
                p.amazon_voted = amazon_voted.find_all('span')[3]['aria-label']
            except:
                p.amazon_voted = ''
            try:
                p.amazon_title = product.find('h5', class_='a-color-base s-line-clamp-2').span.string
            except:
                p.amazon_title = ''
            try:
                p.amazon_link = 'https://www.amazon.com' + product.find('h5', class_='a-color-base s-line-clamp-2').a[
                    'href']
            except:
                p.amazon_link = ''

    driver.close()


def collect_data_from_flipkart(walmart_mobile):
    for m in walmart_mobile:
        flip = flipkart_url + m.search_term
        print(flip)
        driver = webdriver.PhantomJS(executable_path='D:\installed\phantomjs.exe')

        driver.get(flip)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        mobile = soup.find('a', class_='_31qSD5')

        if (mobile):
            link = mobile['href']
            m.flipkart_link = 'https://www.flipkart.com' + link
            m.flipkart_rating = mobile.find('div', class_='hGSR34').text
            m.flipkart_voted = mobile.find('span', class_='_38sUEc').span.span.text
            flipkart_price = mobile.find('div', class_='_1vC4OE _2rQ-NK').string
            m.flipkart_price = flipkart_price[1:]
        else:
            m.flipkart_link = ''
            m.flipkart_rating = ''
            m.flipkart_voted = ''
            m.flipkart_price = ''


# calling functions
walmart_laptop = collect_data_from_walmart(walmart_laptop_url, 'laptop')
collect_data_from_amzn(walmart_laptop)
csv_conversion(walmart_laptop, 'laptop.csv', 'laptop')

walmart_mobile = collect_data_from_walmart(walmart_mobile_url, 'mobile')
collect_data_from_flipkart(walmart_mobile)
csv_conversion(walmart_mobile, 'mobile.csv', 'mobile')

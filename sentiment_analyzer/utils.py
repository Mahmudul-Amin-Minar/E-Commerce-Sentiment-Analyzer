import re
import requests
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

# imgTagWrapperId
# productTitle

# daraz == item-content
url = 'https://www.daraz.com.bd/products/vr-box-virtual-reality-3d-glasses-black-i2301815-s62110081.html?spm=a2a0e.searchlistcategory.list.3.3d0f42c2dCg6Ok&search=1'
x = re.findall('(-i)(\d+)(-)', url)[0][1]
print(x)
# response = requests.get('https://my.daraz.com.bd/pdp/review/getReviewList?itemId=2301815&pageSize=5&filter=0&sort=0&pageNo=66')
# json_data = json.loads(response.text)
# sorted_list = json.dumps(json_data, indent=4, sort_keys=True)
# print(sorted_list)
#
#
# reviews = json_data.get('model').get('items')
# print(len(reviews))
# for i in reviews:
#     rev = i.get('reviewContent')
#     print(rev)
# driver = webdriver.Chrome(executable_path='D:\installed\chromedriver.exe', options=chrome_options)
# daraz_review_dict = []
#
# url = url
# driver.get(url)
# soup = BeautifulSoup(driver.page_source, 'lxml')
# pagination = soup.find_all('div', class_='next-pagination-list')[0]
# page_number = pagination.find_all('button')[-1].text
# page_number = int(page_number)

# for i in page_number:
#     j = 0
#     if i < 4:
#         next_page = driver.find_elements_by_xpath(
#             f"//*[@id=\"module_product_review\"]/div/div[3]/div[2]/div/div/button[{i}]")
#     if i >= 4 and (page_number - i) >= 3:
#         next_page = driver.find_elements_by_xpath(
#             "//*[@id=\"module_product_review\"]/div/div[3]/div[2]/div/div/button[4]")
#     if i > 4 and (page_number - i) < 3:
#         next_page = driver.find_elements_by_xpath(
#             f"//*[@id=\"module_product_review\"]/div/div[3]/div[2]/div/div/button[{3 + j}]")
#         j += 1

# print(page_number)

# next_button = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
#
# # comment extraction goes here --->>>>
# total_reviews = soup.find_all('div', class_='item-content')
# print(total_reviews)

# https://www.daraz.com.bd/products/mrs-rack-5-step-wo-tray-blue-i2151370-s48783396.html?spm=a2a0e.11884278.1008.dstorelist_2_3.42cd43a6AB4gG8&acm=20180501004&scm=1007.21294.114653.100200300000000
# https://www.daraz.com.bd/products/mrs-rack-5-step-wo-tray-blue-i2151370-s48783396.html?spm=a2a0e.11884278.1008.dstorelist_2_3.42cd43a6AB4gG8&acm=20180501004&scm=1007.21294.114653.100200300000000
# https://www.daraz.com.bd/products/vr-box-virtual-reality-3d-glasses-black-i2301815-s62110081.html?spm=a2a0e.searchlistcategory.list.3.3d0f42c2dCg6Ok&search=1
# https://my.daraz.com.bd/pdp/review/getReviewList?itemId=2301815&pageSize=5&filter=0&sort=0&pageNo=3
# https://my.daraz.com.bd/pdp/review/getReviewList?itemId=2301815&pageSize=5&filter=0&sort=0&pageNo=3
# https://my.daraz.com.bd/pdp/review/getReviewList?itemId=2301815&pageSize=5&filter=0&sort=0&pageNo=4
# https://my.daraz.com.bd/pdp/review/getReviewList?itemId=481765&pageSize=5&filter=0&sort=0&pageNo=2
# a2a0e.pdp.ratings_reviews.i0.294f17b9S5Op3S
# 1 === //*[@id="module_product_review"]/div/div[3]/div[2]/div/div/button[1]
# 2 === //*[@id="module_product_review"]/div/div[3]/div[2]/div/div/button[2]
# 3 === //*[@id="module_product_review"]/div/div[3]/div[2]/div/div/button[3]
# 4 === //*[@id="module_product_review"]/div/div[3]/div[2]/div/div/button[4]
# 5 === //*[@id="module_product_review"]/div/div[3]/div[2]/div/div/button[3]
# 66 === //*[@id="module_product_review"]/div/div[3]/div[2]/div/div/button[4]

# 65%5

# driver.quit()

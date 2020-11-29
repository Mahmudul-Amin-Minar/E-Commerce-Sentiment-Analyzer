import re
import requests
import json
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import re
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")


# Create your views here.

class AmazonReview:
    def __init__(self, **kwargs):
        self.rating = kwargs['rating']
        self.title = kwargs['title']
        self.review = kwargs['review_text']
        self.author = kwargs['author']
        self.date = kwargs['date']
        self.sentiment = kwargs['sentiment_cat']
        self.g_rating = kwargs['g_rating']


def index(request):
    # template = loader.get_template('')
    a = [1, 2, 3, 4, 5]
    return render(request, 'sentiment_analyzer/sentiment.html', {'a': a})


def sentiment_check(request):
    text = request.POST.get('text')
    if text is None:
        return render(request, 'sentiment_analyzer/single.html')
    # print(type(text))
    # sent = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    analyser = SentimentIntensityAnalyzer()
    analysis = analyser.polarity_scores(text)
    sentiment = ''
    if analysis['compound'] >= 0.4:
        sentiment = 'P'
    elif analysis['compound'] < 0.4 and analysis['compound'] > -0.6:
        sentiment = 'N'
    elif analysis['compound'] <= -0.6:
        sentiment = 'Neg'
    return render(request, 'sentiment_analyzer/single.html', {'t': analysis, 'text': text, 'sentiment': sentiment})


def features(request):
    return render(request, 'sentiment_analyzer/features.html')


def amazon_review(request):
    positive = 0
    negative = 0
    neutral = 0
    total_g_rating = 0
    url = request.POST.get('url')
    site = url.split('.')[1]

    driver = webdriver.Chrome(executable_path='D:\installed\chromedriver.exe', options=chrome_options)
    amazon_review_dict = []

    if site == 'amazon':
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # print(soup.find('span', id='productTitle'))
        product_title = soup.find('span', id='productTitle').string.strip()
        # product_title = ''
        product_image = soup.find('img', id='landingImage')['src']
        total_rating = soup.find('span', class_='a-size-medium a-color-base').text.split(' ')[0]

        reviews_link = 'https://www.amazon.com' + soup.find('a', class_='a-link-emphasis a-text-bold')['href']
        driver.get(reviews_link)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # comment extraction goes here --->>>>
        total_reviews = soup.find_all('div', class_='a-section review aok-relative')

        analyser = SentimentIntensityAnalyzer()

        for review in total_reviews:
            author = review.find('span', class_='a-profile-name').string
            rating = review.find('span', class_='a-icon-alt').string
            date = review.find('span', class_='a-size-base a-color-secondary review-date').string
            title = (review.find('a',
                                 class_='a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold')).find(
                'span').string
            review_text = (review.find('span', class_='a-size-base review-text review-text-content')).find('span').text

            analysis = analyser.polarity_scores(review_text)
            sentiment_cat = ''
            if analysis['compound'] >= 0.4:
                sentiment_cat = 'P'
                positive += 1
                if analysis['compound'] >= 0.7:
                    g_rating = 5
                elif analysis['compound'] >= 0.4:
                    g_rating = 4
                elif analysis['compound'] >= 0.2:
                    g_rating = 3
            elif analysis['compound'] < 0.4 and analysis['compound'] > -0.6:
                sentiment_cat = 'N'
                neutral += 1
                if analysis['compound'] >= 0.2:
                    g_rating = 3
                elif analysis['compound'] >= -0.4:
                    g_rating = 2
            elif analysis['compound'] <= -0.6:
                sentiment_cat = 'Neg'
                negative += 1
                g_rating = 1

            total_g_rating += g_rating
            amazon_review_obj = AmazonReview(author=author, rating=rating[:3], date=date, title=title,
                                             review_text=review_text, sentiment_cat=sentiment_cat, g_rating=g_rating)
            amazon_review_dict.append(amazon_review_obj)

        try:
            next_page = 'https://www.amazon.com' + soup.find('li', class_='a-last').a['href']
        except:
            next_page = None

        while (next_page != None):
            # comment extraction goes here --->>>>
            driver.get(next_page)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            total_reviews = soup.find_all('div', class_='a-section review aok-relative')

            for review in total_reviews:
                author = review.find('span', class_='a-profile-name').string
                rating = review.find('span', class_='a-icon-alt').string
                date = review.find('span', class_='a-size-base a-color-secondary review-date').string
                title = (review.find('a',
                                     class_='a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold')).find(
                    'span').string
                review_text = (review.find('span', class_='a-size-base review-text review-text-content')).find('span').text

                analysis = analyser.polarity_scores(review_text)
                sentiment_cat = ''
                if analysis['compound'] >= 0.4:
                    sentiment_cat = 'P'
                    positive += 1
                    if analysis['compound'] >= 0.7:
                        g_rating = 5
                    elif analysis['compound'] >= 0.4:
                        g_rating = 4
                    elif analysis['compound'] >= 0.2:
                        g_rating = 3
                elif analysis['compound'] < 0.4 and analysis['compound'] > -0.6:
                    sentiment_cat = 'N'
                    neutral += 1
                    if analysis['compound'] >= 0.2:
                        g_rating = 3
                    elif analysis['compound'] >= -0.4:
                        g_rating = 2
                elif analysis['compound'] <= -0.6:
                    sentiment_cat = 'Neg'
                    negative += 1
                    g_rating = 1

                total_g_rating += g_rating
                amazon_review_obj = AmazonReview(author=author, rating=rating[:3], date=date, title=title,
                                                 review_text=review_text, sentiment_cat=sentiment_cat, g_rating=g_rating)
                amazon_review_dict.append(amazon_review_obj)

            try:
                next_page = 'https://www.amazon.com' + soup.find('li', class_='a-last').a['href']
            except:
                next_page = None

        driver.quit()
        total_given_rating = total_g_rating / (positive + negative + neutral)
        return render(request, 'sentiment_analyzer/show_table.html', {'review_dict': amazon_review_dict,
                                                                      'product_title': product_title,
                                                                      'product_image': product_image,
                                                                      'positive': positive,
                                                                      'negative': negative,
                                                                      'neutral': neutral,
                                                                      'total' : positive+neutral+negative,
                                                                      'total_rating': total_rating,
                                                                      'total_g_rating': round(total_given_rating, 1)})

    elif site == 'daraz':
        chrome_options.add_argument("--headless")

        daraz_review_dict = []
        positive = 0
        negative = 0
        neutral = 0

        total_g_rating = 0

        product_id = re.findall('(-i)(\d+)(-)', url)
        product_id = product_id[0][1]
        print(product_id)

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        product_title = soup.find('span', class_='pdp-mod-product-badge-title').text
        product_image = soup.find('img', class_='pdp-mod-common-image gallery-preview-panel__image')['src']
        total_rating = soup.find('span', class_='score-average').text

        pagination = soup.find_all('div', class_='next-pagination-list')[0]
        page_number = pagination.find_all('button')[-1].text
        page_number = int(page_number)

        analyser = SentimentIntensityAnalyzer()

        for i in range(1, page_number):
            json_url = f'https://my.daraz.com.bd/pdp/review/getReviewList?itemId={product_id}&pageSize=5&filter=0&sort=0&pageNo={i}'

            response = requests.get(json_url)

            if response:
                json_data = json.loads(response.text)
                reviews = json_data.get('model').get('items')
                # print(len(reviews))

                for review in reviews:
                    author = review.get('buyerName')
                    rating = review.get('rating')
                    date = review.get('reviewTime')
                    title = review.get('reviewTitle')
                    review_text = review.get('reviewContent')



                    tran_review_text = review_text
                    if review_text:
                        print(review_text)
                        original_review_text = TextBlob(review_text)

                        if original_review_text.detect_language() == 'bn':
                            try:
                                tran_review_text = original_review_text.translate(to='en')
                            except:
                                tran_review_text = ''
                            # print(tran_review_text)

                        try:
                            analysis = analyser.polarity_scores(tran_review_text)
                            if analysis['compound'] >= 0.4:
                                sentiment_cat = 'P'
                                positive += 1
                                if analysis['compound'] >= 0.7:
                                    g_rating = 5
                                elif analysis['compound'] >= 0.4:
                                    g_rating = 4
                                elif analysis['compound'] >= 0.2:
                                    g_rating = 3
                            elif analysis['compound'] < 0.4 and analysis['compound'] > -0.6:
                                sentiment_cat = 'N'
                                neutral += 1
                                if analysis['compound'] >= 0.2:
                                    g_rating = 3
                                elif analysis['compound'] >= -0.4:
                                    g_rating = 2
                            elif analysis['compound'] <= -0.6:
                                sentiment_cat = 'Neg'
                                negative += 1
                                g_rating = 1
                        except:
                            sentiment_cat = 'N'
                            neutral += 1
                            g_rating = 3

                        total_g_rating += g_rating

                        daraz_review_obj = AmazonReview(author=author, rating=rating, date=date, title=title,
                                                            review_text=review_text, sentiment_cat=sentiment_cat, g_rating=g_rating)
                        daraz_review_dict.append(daraz_review_obj)
            else:
                json_data = ''
            # sorted_list = json.dumps(json_data, indent=4, sort_keys=True)
            # print(sorted_list)


        driver.quit()
        total_given_rating = total_g_rating/(positive+negative+neutral)
        return render(request, 'sentiment_analyzer/show_table.html', {'review_dict': daraz_review_dict,
                                                                      'product_title': product_title,
                                                                      'product_image': product_image,
                                                                      'positive': positive,
                                                                      'negative': negative,
                                                                      'neutral': neutral,
                                                                      'total': positive + neutral + negative,
                                                                      'total_rating': total_rating,
                                                                      'total_g_rating': round(total_given_rating, 1)})
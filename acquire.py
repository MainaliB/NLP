from requests import get
import pandas as pd
from bs4 import BeautifulSoup 
import os



def get_blog_articles():
    '''Takes in a list of url, parses it using Beautiful Soup and returns a list of dictionaries
    of title as key and content as value'''
    lst = []

    url = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
      'https://codeup.com/data-science-myths/',
      'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
      'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
       'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/',
       'https://codeup.com/introducing-salary-refund-guarantee/',
      'https://codeup.com/new-scholarship/']
    for elem in url:
        headers = {'User-Agent': 'Codeup Data Science'}
        response = get(elem, headers = headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string
        article = soup.find('div', class_ = 'jupiterx-post-content')
        article_text = article.text
        item = {
            'title': title,
            'content': article_text
        }
        lst.append(item)

        df = pd.DataFrame(lst)
    return df



# Create a helper function that requests and parses HTML returning a soup object.

def make_soup(url):
    '''
    This helper function takes in a url and requests and parses HTML
    returning a soup object.
    '''
    headers = {'User-Agent': 'Codeup Data Science'} 
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup





def get_news_articles(cached=False):
    '''
    This function with default cached == False does a fresh scrape of inshort pages with topics 
    business, sports, technology, and entertainment and writes the returned df to a json file.
    cached == True returns a df read in from a json file.
    '''
    # option to read in a json file instead of scrape for df
    if cached == True:
        df = pd.read_json('articles.json')
        
    # cached == False completes a fresh scrape for df    
    else:
    
        # Set base_url that will be used in get request
        base_url = 'https://inshorts.com/en/read/'
        
        # List of topics to scrape
        topics = ['business', 'sports', 'technology', 'entertainment']
        
        # Create an empty list, articles, to hold our dictionaries
        articles = []

        for topic in topics:
            
            # Create url with topic endpoint
            topic_url = base_url + topic
            
            # Make request and soup object using helper
            soup = make_soup(topic_url)

            # Scrape a ResultSet of all the news cards on the page
            cards = soup.find_all('div', class_='news-card')

            # Loop through each news card on the page and get what we want
            for card in cards:
                title = card.find('span', itemprop='headline' ).text
                author = card.find('span', class_='author').text
                content = card.find('div', itemprop='articleBody').text

                # Create a dictionary, article, for each news card
                article = ({'topic': topic, 
                            'title': title, 
                            'author': author, 
                            'content': content})

                # Add the dictionary, article, to our list of dictionaries, articles.
                articles.append(article)
            
        # Create a DataFrame from list of dictionaries
        df = pd.DataFrame(articles)
        
        # Write df to json file for future use
        df.to_json('articles.json')
    
    return df
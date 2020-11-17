import nltk

import acquire
import pandas as pd
import os
from bs4 import BeautifulSoup

import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords


# function to perform basic cleaning
def basic_clean(string):
    '''Takes in a string and performs basic cleaning like removing unnecessary characters, accents'''

    string = string.lower()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')\
            .decode('utf-8', 'ignore')
    string = re.sub(r"[^a-z0-9\s]", '', string)
    
    return string
    
# function to tokenize 
def tokenize(string):
    '''Takes in a string and tokenizes the string'''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    string = tokenizer.tokenize(string, return_str = True)
    return string


# function to stem
def stem(string):
    '''Takes in a string and returns a string after applying stemming to all the words '''

    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    string_stemmed = ' '.join(stems)
    return string_stemmed


# function to lemmatize
def lemmatize(string):

    '''Accepts some text and return the text after applying lemmatization to each word.'''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    string_lemmatized = ' '.join(lemmas)
    
    return string_lemmatized


# function to remove stop words
def remove_stopwords(string, extra_words = [], exclude_words= []):
    '''Accepts some text and return the text after removing all the stopwords.
    Also takes two optional parameters, extra_words and exclude_words.
    These parameters define any additional stop words to include, and any words that we don't want to remove.'''

    stopword_list = stopwords.words('english')
    for word in extra_words:
        stopword_list.append(word)
    for word in exclude_words:
        stopword_list.remove(word)
    words = string.split()
    filtered_words = [w for w in words if w not in stopword_list]
    string_without_stopwords = ' '.join(filtered_words)
    return string_without_stopwords


# function to prepare data
def prepare_data(df, column, extra_words = [], exclude_words = []):
    '''Takes in the dataframe, column to work on, extra words to add on to stopwords list, 
    words to exclude from stopwords list and returns a dataframe with additional columns that 
    are clean, stemmed, and lemmatized'''
    
    df['clean'] = df[column].apply(basic_clean).apply(tokenize).apply(remove_stopwords)
    df['stemmed'] = df['clean'].apply(stem)
    df['lemmatized'] = df['clean'].apply(lemmatize)
    return df
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
from random import randint
import os
import sys


def scroll(browser): #infinite scrolling down- eact time that gets to the end
    try_to_scroll = 0
    last_pos = browser.execute_script("return window.pageYOffset;")
    i = 0
    while True:
        i += 1
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(1)
        new_pos = browser.execute_script("return window.pageYOffset;")
        if last_pos == new_pos:
            try_to_scroll += 1
            if try_to_scroll >= 3:
                return False
            else:
                time.sleep(2) #before new try
        else:
            last_pos = new_pos
            break
    return True


def count_words():
    words = []
    words_dict = {}
    tweets_doc = open("tweets.txt", "r")
    lines = tweets_doc.readlines()
    for line in lines[1:]:
        if line.startswith("tweet number"):
            continue
        else:
            words.extend(line.split())
    chars = [',', '.', '!', '?', '״', '"', ':', '(', ')', '*']
    for word in words:
        for char in chars:
            if char in word:
                word = word.replace(char, "")
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1
    count_word_doc = open("countWords.txt", "a")
    for word in words_dict:
        count_word_doc.write(word + " : " + str(words_dict[word]) + "\n")


def tags_scraper(tags_dict, post, user, browser, posted_name, count_tags_doc):
    section = post.find_elements_by_css_selector('*[class = "r-18u37iz"]')
    browser.implicitly_wait(2)
    for t in section:
        if t.text[0]=='@' and posted_name == user:
            if t.text in tags_dict:
                tags_dict[t.text] += 1
            else:
                tags_dict[t.text] = 1


def hash_scraper(hash_dict, post, user, browser, posted_name, count_hash_doc):
    section = post.find_elements_by_css_selector('*[class = "r-18u37iz"]')
    browser.implicitly_wait(2)
    if section is not None:
        for h in section:
            if h.text[0]=='#'and posted_name == user:
                if h.text in hash_dict:
                    hash_dict[h.text] += 1
                else:
                    hash_dict[h.text] = 1


def tweet_scraper(id_tweets, post, tweets_doc, count):
    try: 
        tweet = post.find_element_by_xpath('./div[2]/div[2]/div[1]//span').text #text of tweet
    except NoSuchElementException:
        tweets_doc.write("tweet number " + str(count) + ": " + "NO TEXT IN THE TWEET." + "\n")
        return
    if tweet not in id_tweets:
        id_tweets.add(''.join(tweet))
        tweets_doc.write("tweet number " + str(count) + ":" + "\n" + tweet + "\n")
    

def main(url):
    webDriverFile = os.path.join(sys.path[0], 'chromedriver')
    os.chmod(webDriverFile, 755)
    browser = webdriver.Chrome(executable_path = webDriverFile)
    browser.get(url)
    browser.maximize_window()
    browser.implicitly_wait(10)
    name = url[20:]
    user = '@' + name

    tweets_doc = open("tweets.txt", "a+")
    tweets_doc.write("Last 100 tweets of {}: \n".format(user))
    count_tags_doc = open("countTags.txt", "a+")
    count_hash_doc = open("countHash.txt", "a+")
    count = 1
    scrolling = True #can scroll
    id_tweets = set()
    tags_dict = {}
    hash_dict = {}

    while count <= 100 and scrolling:
        tweets = browser.find_elements_by_xpath('//div[@data-testid="tweet"]') #gather the tweets in Amit Segal's page
        for post in tweets[-10:]:
            posted_name = post.find_element_by_xpath('.//span[contains(text(), "@")]').text #by analyzing the HTML file- looking for the name of the publisher
            if posted_name == user:
                tweet_scraper(id_tweets, post, tweets_doc, count)
                count += 1
            tags_scraper(tags_dict, post, user, browser, posted_name, count_tags_doc)
            browser.implicitly_wait(2)
            hash_scraper(hash_dict, post, user, browser, posted_name, count_hash_doc)
            if count > 100:
                break
        scrolling = scroll(browser)
    
    for tag in tags_dict:
        count_tags_doc.write(tag + " : " + str(tags_dict[tag]) + "\n")
    for hashtag in hash_dict:
        count_hash_doc.write(hashtag + " : " + str(hash_dict[hashtag]) + "\n")
    count_words()

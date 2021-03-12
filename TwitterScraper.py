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


def infiniteScroll(browser): #infinite scrolling down- eact time that gets to the end
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


def countWords():
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
    countWordDoc = open("countWords.txt", "a")
    for word in words_dict:
        countWordDoc.write(word + " : " + str(words_dict[word]) + "\n")


def tagsScraper(tagsDict, post, user, browser, postedName, countTagsDoc):
    section = post.find_elements_by_css_selector('*[class = "r-18u37iz"]')
    browser.implicitly_wait(2)
    for t in section:
        if t.text[0]=='@' and postedName == user:
            if t.text in tagsDict:
                tagsDict[t.text] += 1
            else:
                tagsDict[t.text] = 1


def hashScraper(hashDict, post, user, browser, postedName, countHashDoc):
    section = post.find_elements_by_css_selector('*[class = "r-18u37iz"]')
    browser.implicitly_wait(2)
    if section is not None:
        for h in section:
            if h.text[0]=='#'and postedName == user:
                if h.text in hashDict:
                    hashDict[h.text] += 1
                else:
                    hashDict[h.text] = 1


def tweetScraper(id_tweets, post, tweets_doc, count):
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
    countTagsDoc = open("countTags.txt", "a+")
    countHashDoc = open("countHash.txt", "a+")
    count = 1
    scrolling = True #can scroll
    id_tweets = set()
    tagsDict = {}
    hashDict = {}

    while count <= 100 and scrolling:
        tweets = browser.find_elements_by_xpath('//div[@data-testid="tweet"]') #gather the tweets in Amit Segal's page
        for post in tweets[-10:]:
            postedName = post.find_element_by_xpath('.//span[contains(text(), "@")]').text #by analyzing the HTML file- looking for the name of the publisher
            if postedName == user:
                tweetScraper(id_tweets, post, tweets_doc, count)
                count += 1
            tagsScraper(tagsDict, post, user, browser, postedName, countTagsDoc)
            browser.implicitly_wait(2)
            hashScraper(hashDict, post, user, browser, postedName, countHashDoc)
            if count > 100:
                break
        scrolling = infiniteScroll(browser)
    
    for tag in tagsDict:
        countTagsDoc.write(tag + " : " + str(tagsDict[tag]) + "\n")
    for hashtag in hashDict:
        countHashDoc.write(hashtag + " : " + str(hashDict[hashtag]) + "\n")
    countWords()

main("https://twitter.com/amit_segal")

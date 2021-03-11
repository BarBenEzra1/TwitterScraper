from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from random import randint
import os
import sys


def infiniteScroll(browser): #infinite scrolling down- eact time that gets to the end
    WAIT = 2
    # Get current height using scrollHeight property that returns the height of the doc body.
    height = browser.execute_script("return document.body.scrollHeight")
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(WAIT) # Wait to load page
    newHeight = browser.execute_script("return document.body.scrollHeight")
    if newHeight == height: #the end of the page
        return 
    height = newHeight


def countWords():
    words = []
    wordsDict = {}
    tweetsDoc = open("tweets.txt", "r")
    lines = tweetsDoc.readlines()
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
        if word in wordsDict:
            wordsDict[word] += 1
        else:
            wordsDict[word] = 1
    countWordDoc = open("countWords.txt", "a")
    for word in wordsDict:
        countWordDoc.write(word + " : " + str(wordsDict[word]) + "\n")


def tagsScraper(post, user, browser, postedName):
    section = post.find_elements_by_css_selector('*[class = "r-18u37iz"]')
    browser.implicitly_wait(2)
    tagsDict = {}
    for t in section:
        if t.text[0]=='@' and postedName == user:
            print(t.text)
    #         if t.text in tagsDict:
    #             tagsDict[t.text] += 1
    #         else:
    #             tagsDict[t.text] = 1
    # countTagsDoc = open("countTags.txt", "a+")
    # for tag in tagsDict:
    #     countTagsDoc.write(tag.text + " : " + str(tagsDict[tag.text]) + "\n")


def hashScraper(post, user, browser, postedName):
    section = post.find_elements_by_css_selector('*[class = "r-18u37iz"]')
    browser.implicitly_wait(2)
    hashDict = {}
    if section is not None:
        for h in section:
            if h.text[0]=='#'and postedName == user:
                print(h.text)
                #if h.text in hashDict:
                    #hashDict[h.text] += 1
                #else:
                    #hashDict[h.text] = 1   
        # countHashDoc = open("countHash.txt", "a+")
        # for hash in hashDict:
        #     countHashDoc.write(hash + " : " + str(hashDict[hash]) + "\n")


def tweetScraper(post, tweetsDoc, count):
    try: 
        tweet = post.find_element_by_xpath('./div[2]/div[2]/div[1]//span').text #text of tweet
    except NoSuchElementException:
        tweetsDoc.write("tweet number " + str(count) + ": " + "NO TEXT IN THE TWEET." + "\n")
        return 
    tweetsDoc.write("tweet number " + str(count) + ":" + "\n" + tweet + "\n")


def main(url):
    webDriverFile = os.path.join(sys.path[0], 'chromedriver')
    os.chmod(webDriverFile, 755)
    browser = webdriver.Chrome(executable_path = webDriverFile)
    browser.get(url)
    browser.maximize_window()
    browser.implicitly_wait(10)
    name = url[20:]
    user = '@' + name

    tweetsDoc = open("tweets.txt", "a+")
    tweetsDoc.write("Last 100 tweets of {}: \n".format(user))
    count = 0
    
    while count <= 100:
        tweets = browser.find_elements_by_xpath('//div[@data-testid="tweet"]') #gather the tweets in Amit Segal's page
        for post in tweets:
            postedName = post.find_element_by_xpath('.//span[contains(text(), "@")]').text #by analyzing the HTML file- looking for the name of the publishe
            tagsScraper(post, user, browser, postedName)
            browser.implicitly_wait(2)
            hashScraper(post, user, browser, postedName)
            if postedName == user:
                tweetScraper(post, tweetsDoc, count)
            count += 1
            if count > 100:
                break
        infiniteScroll(browser)

    countWords()

main("https://twitter.com/amit_segal")

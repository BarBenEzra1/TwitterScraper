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
    WAIT  = 3
    # Get current height using scrollHeight property that returns the height of the doc body.
    height = browser.execute_script("return document.body.scrollHeight")
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(WAIT) # Wait to load page
    newHeight = browser.execute_script("return document.body.scrollHeight")
    if newHeight == height: #the end of the page
        return 0
    height = newHeight
    return 1


def countWords():
    words = []
    wordsDict = {}
    tweetsDoc = open("tweetsAmit.txt", "r")
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


def tagsScraper(post):
    postedName = post.find_element_by_xpath('.//span[contains(text(), "@")]').text #by analyzing the HTML file- looking for the name of the publishe
    section = post.find_elements_by_xpath('./div[2]/div[2]/div[1]//div')
    for t in section:
        if t.text[0]=='@' and postedName == "@amit_segal":
            print(t.text)
    # tagsDict = {}
    # for tag in tags:
    #     if '@amit_segal' not in tag.text:
    #         if tag in tagsDict:
    #             tagsDict[tag] += 1
    #         else:
    #             tagsDict[tag] = 1
    # countTagsDoc = open("countTags.txt", "a+")
    # for t in tagsDict:
    #     countTagsDoc.write(t.text + " : " + str(tagsDict[t]) + "\n")


def hashScraper(post):
    postedName = post.find_element_by_xpath('.//span[contains(text(), "@")]').text #by analyzing the HTML file- looking for the name of the publishe
    section = post.find_elements_by_xpath('./div[2]/div[2]/div[1]//div')
    if section is not None:
        for h in section:
            if h.text[0]=='#'and postedName == "@amit_segal":
                print(h.text)
    #hashtags = section.find_elements_by_partial_link_text('#')
    # hashDict = {}
    # for hashtag in hashtags:
    #     if hashtag in hashDict:
    #         hashDict[hashtag] += 1
    #     else:
    #         hashDict[hashtag] = 1
    # countHashDoc = open("countHash.txt", "a+")
    # for h in hashDict:
    #     countHashDoc.write(h + " : " + str(hashDict[h]) + "\n")


def tweetScraper(post, tweetsDoc, count):
    postedName = post.find_element_by_xpath('.//span[contains(text(), "@")]').text #by analyzing the HTML file- looking for the name of the publisher
    if postedName == "@amit_segal":
        try: 
            tweet = post.find_element_by_xpath('./div[2]/div[2]/div[1]//span').text #text of tweet
        except NoSuchElementException:
            tweetsDoc.write("tweet number " + str(count) + ": " + "NO TEXT IN THE TWEET" + "\n")
            return 
        tweetsDoc.write("tweet number " + str(count) + ":" + "\n" + tweet + "\n")


def main():
    webDriverFile = os.path.join(sys.path[0], 'chromedriver')
    os.chmod(webDriverFile, 755)
    browser = webdriver.Chrome(executable_path = webDriverFile)
    browser.get("https://twitter.com/amit_segal")
    browser.maximize_window()
    browser.implicitly_wait(20)

    tweetsDoc = open("tweetsAmit.txt", "a+")
    tweetsDoc.write("Last 100 tweets of Amit Segal: \n")
    count = 0
    
    while count <= 100:
        tweets = browser.find_elements_by_xpath('//div[@data-testid="tweet"]') #gather the tweets in Amit Segal's page
        for post in tweets:
            tagsScraper(post)
            browser.implicitly_wait(2)
            hashScraper(post)
            browser.implicitly_wait(2)
            tweetScraper(post, tweetsDoc, count)
            count += 1
            if count > 100:
                break
        infiniteScroll(browser)

    countWords()

main()

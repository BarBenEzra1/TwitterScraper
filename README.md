# TwitterScraper
This is a Twitter Scraper project based Selenium Python.
My IDE : Visual Studio Code.
The code logs in to Twitter, takes Amit Segal's last 100 tweets and provides the following output files:
1. **Tweets List** - tweets.txt file
1. **Hashtag list**- countHash.txt file
2. **Mention list**- countTags.txt file
3. **Word statistics** - countWords.txt file

**The functions in the code:**
1. **scroll(browser)** - this function gets the open browser as a parameter and scroll it down. The browser will try at most 3 times in case it's fails to scroll (might happen if the page wasn't loaded yet, the new and last positions are the same). The scrolling lasts till the main function runs over 100 tweets.
2. **tweet_scraper(id_tweets, post, tweets_doc, count)** - this function gets a set of all last tweets, a new tweet element from the HTML code, the tweet_doc (which is tweets.txt file that was opened in the main) and the count variable (used for the printing). The function extract the text part from the given tweet element and prints it in the tweets.txt file in case it is not in the given id_tweets set.
4. **tags_scraper(tags_dict, post, user, browser, posted_name, count_tags_doc)** - this function gets a dictionary used for counting the occurences of each tag mention, a tweet element from the HTML code, the user, the browser and the user that posted the given tweet. The function looks for all the tag mentions (@somename) and count them. The function creates the count_tags.txt file and prints the counting results in it.
5. **count_words()** - this function opens the tweets.txt file and count the amount from each word is Amit's last 100 tweets. The function creates the countWords.txt file and prints the counting results in it.
6. **hash_scraper(hash_dict, post, user, browser, posted_name, count_hash_do)** - this function gets a dictionary used for counting the occurences of each hashtag, a tweet element from the HTML code, the user, the browser and the user that posted the given tweet. The function looks for all the hashtags (#somehashtag) and count them. The function creates the count_hash.txt file and prints the counting results in it.
7. **main(url)** - this functions opens the browser and set its page to the URL (of Amit Segal's Twitter page). Then, it calls 100 times in a loop to the above functions and they create the required files.

**Run the code:**
In order to run the code- download the TwitterScraper.zip to your computer and read the README.md file (😜).
Open the code in your IDE and make sure you have a Selenium installed in your pc, otherwise, use the "pip install selenium" command.
Now, run the code in terminal from the path to the TwitterScraper-main and wait (!) for the Chrome browser that has been opened at the beginning to get **closed**. Selenium basically sends queries to the HTTP server for each Selenium command and interupting the process, such as, changing the URL of the Chrome browser or scroll the page by yourself (etc.) may cause errors.
The running process might take approximately 5 minutes since waiting for the HTTP server to send its answer takes time. 

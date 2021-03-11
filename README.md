# TwitterScraper
This is a Twitter Scraper project based Selenium Python.
My IDE : Visual Studio Code.
The code logs in to Twitter, takes Amit Segal's last 100 tweets and provides the following output files:
1. **Tweets List** - tweetsAmit.txt file
1. **Hashtag list**- countHash.txt file
2. **Mention list**- countTags.txt file
3. **Word statistics** - countWords.txt file
4. Bonus: write tests

The functions in the code:
1. **infiniteScroll(browser)** - this function gets the open browser as a parameter and scroll it down. The scrolling lasts till the main function runs over 100      tweets.
2. **tweetScraper(post, tweetsDoc, count)** - this function gets a tweet element from the HTML code, the tweetDoc (which is weetsAmit.txt file that was opened in the main) and the count variable (used for the printing). The function extract the text part from the tweet element and prints it in the weetsAmit.txt file.
4. **tagsScraper(post)** - this function gets a tweet element from the HTML code, looks for all the mentions (@somename) and count them. The function creates the countTags.txt file and prints the counting results in it.
5. **countWords()** - this function opens the tweetsAmit.txt file and count the amount from each word is Amit's last 100 tweets. The function creates the countWords.txt file and prints the counting results in it.
6. **hashScraper(post)** - this function gets a tweet element from the HTML code, looks for all the hashtags (@somehashtag) and count them. The function creates the countHash.txt file and prints the counting results in it.
7. main() - this functions opens the browser and calls Amit Segal's Twitter page. Then, it calls 100 times in a loop to the above functions and they create the required files.


**Run the code:**
In order to run the code- download the TwitterScraper.zip to your computer and read the README.md file (😜).
Open the code in your IDE and make sure you have a Selenium installed in your pc, otherwise, use the "pip install selenium" command.
Now, run the code and wait (!) for the Chrome browser that has been opened at the beginning to get closed. Selenium basically sends queries to the HTTP server for each selenium command and interupting the process, such as, changing the URL of the Chrome browser or scroll the page by yourself (etc.) may cause errors.

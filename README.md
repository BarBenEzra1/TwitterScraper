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
1. infiniteScroll(browser) - this function gets the open browser as a parameter and scroll it down. The scrolling lasts till the main function runs over 100 tweets.
2. tagsScraper(post) - this function gets a tweet element from the HTML code, looks for all the mentions (@somename) and count them. The function creates the countTags.txt file and prints the counting results in it.
3. countWords() - this function opens the tweetsAmit.txt file and count the amount from each word is Amit's last 100 tweets. The function creates the countWords.txt file and prints the counting results in it.

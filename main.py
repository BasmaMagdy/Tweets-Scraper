import requests
from bs4 import BeautifulSoup
import re
import time

# List of Twitter account URLs to monitor
twitter_accounts = [
    "https://twitter.com/Mr_Derivatives",
    "https://twitter.com/warrior_0719",
    "https://twitter.com/ChartingProdigy",
    "https://twitter.com/allstarcharts",
    "https://twitter.com/yuriymatso",
    "https://twitter.com/TriggerTrades",
    "https://twitter.com/AdamMancini4",
    "https://twitter.com/CordovaTrades",
    "https://twitter.com/Barchart",
    "https://twitter.com/RoyLMattox"
]

stock_symbol = ["$TSLA"]

# Time interval in seconds for scraping session
scraping_interval = 600

def scrape_tweets(account_url, stock_symbol):
    try:
        response = requests.get(account_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            tweets = soup.find_all("div", class_="css-901oao r-1re7ezh r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
            
            mentions_count = 0
            for tweet in tweets:
                tweet_text = tweet.get_text()
                if re.search(re.escape(stock_symbol), tweet_text):
                    mentions_count += 1
            
            return mentions_count
        else:
            print(f"Failed to retrieve tweets from {account_url}")
            return 0
    except Exception as e:
        print(f"Error occurred while scraping {account_url}: {str(e)}")
        return 0

def monitor_twitter_accounts(accounts, stock_symbol, interval):
    while True:
        print(f"Monitoring started at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        for account_url in accounts:
            mentions_count = scrape_tweets(account_url, stock_symbol)
            print(f"'{stock_symbol}' was mentioned '{mentions_count}' times in the last {interval / 60} minutes from {account_url}")
        print(f"Waiting for next scraping session in {interval / 60} minutes...")
        time.sleep(interval)

if __name__ == "__main__":
    monitor_twitter_accounts(twitter_accounts, stock_symbol, scraping_interval)

def scrape_twitter_account(account_url, stock_symbol):
    try:
        response = requests.get(account_url)
        response.raise_for_status()  

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {account_url}: {e}")
        return 0
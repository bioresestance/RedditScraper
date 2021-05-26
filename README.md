# RedditScraper

## Overview
Reddit Scraper is a python script that goes to Reddit and grabs, filters and downloads desired content to the PC or server running it.

## Features

* Automatically download as many, or as little files from your favorite subreddits
* Filter out all unwanted content so you only download the files you really want.
* Set script to run periodically, so you always have the latest reddit files.
* Store files based on subreddit or date, so you always know where and when the files came from.


## How to Use

1. Follow the instructions [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to create a Reddit app and retrieve needed login information.
2. Make sure the latest python interpreter is installed on the PC running the script.
3. Run `pip install -r pyLibs.txt` from the project folder to install needed libraries.
4. Run the python script for the first time to generate the default config file; `python RedditScraper.py`
5. In the newly created "rsConfig.yml" file, fill in at least the "credentials" section with the information gathered in step 1.
6. Adjust any of the other configuration item as wanted.
7. Run the script again, as before, and now the script will retrieve and download files as setup in the config file.


## Features to come
- [ ] Create a Dockerfile to easily run the script in a known environment
- [ ] Add a log file to dump all log information. Currently only writes to the console.
- [ ] Add support to download either Reddit of other site albums. Currently only supports single file per post download.
- [ ] Add more then one download location. This will allow storing files in separate folders based on some filter.

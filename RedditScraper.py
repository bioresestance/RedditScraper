#!/usr/bin/python

# Libraries
import praw
import requests
import sys
import concurrent.futures
import os  
import logging as log
from urllib.parse import urlparse

# Local files
from rsConfig import rsConfig


class rsScraper:

    def __init__(self, config: rsConfig):
        self.config = config


    def login_to_reddit(self):
        credentials = self.config.credentials
        try:
            # Attempt to login to reddit using the provided credential
            self.reddit = praw.Reddit(  client_id=credentials['client_id'], 
                                        client_secret=credentials['client_secret'], 
                                        user_agent=credentials['user_agent'],
                                        username=credentials['username'],
                                        password=credentials['password'])
        except:
            self.reddit = None
                        


    def get_subscribed_subreddits(self, user, num: int):
        if num == 0:
            return list(user.subreddits(limit=None))
        else:
            return list(user.subreddits(limit=num))



    def filter_and_get_posts(self, posts, subreddit):

        found = 0
        curr_post = 0
        post_list = []

        try:
            for post in posts: 
                curr_post = curr_post + 1
                # Filter post
                if  not post.stickied \
                    and post.over_18 == self.config.filters['allow_nsfw'] \
                    and post.url.endswith(tuple(self.config.filters['white_list_file'])):

                    # Create a tuple of URL and Filename and source subreddit for the post. Add to list.
                    post_list.append( (os.path.basename(urlparse(post.url).path), post.url, subreddit.display_name) )
                    found += 1

                # Once we have found enough valid posts or we reached max searches, exit loop
                if found >= self.config.runtime['default_entries'] or curr_post >= self.config.runtime['max_attempts'] :
                    print(f'Found {found} files from {subreddit.display_name}')
                    break
        except Exception as e:
            print("Unable to filter posts. ")

        return post_list



    def download_files(self, post):
        

        filename = post[0]
        # Now lets download the file
        req = requests.get(post[1])

        file_path = ''

        # If files are to be saved in separate Sub folders.
        if config.output['separate_by_sub']:
            # Create the file path in sub folder. path = "'Base path' / 'configured output folder' / 'subreddit name' /"
            file_path = f'{self.base_path}/{post[2]}/'
        else:
            # Create the file path in base configured path. path = "'Base path' / 'configured output folder' /"
            file_path = f'{self.base_path}/'

        # Path does not exist, so lets create it.
        if not os.path.exists(file_path):
            os.mkdir(file_path)
            
        with open( file_path + filename, "wb" ) as f:
            f.write(req.content)

    
    def run(self):

        # Get the base path to save the files to. If it does not exist, create it.
        self.base_path = f'{os.getcwd()}/{self.config.output["output_folder"]}'
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)

        # Attempt to login into Reddit with the provided credentials.
        self.login_to_reddit()

        # Error Logging in, so bail
        if self.reddit == None:
            print("Unable to log into Reddit with the provided Credentials. Please Check the 'rsConfig.yml' config file!")
            exit()

        post_list = []

        # Get all the posts from the subreddits.
        for subreddit in self.get_subscribed_subreddits(self.reddit.user, self.config.runtime['limit_sr']):
            # Get the top posts of the day, and filter them based on config
            post_list += self.filter_and_get_posts(subreddit.hot(limit=None), subreddit)

        print(f'Downloading {len(post_list)} files')

        # Go through each post and download file. Splitting up the work for multi-threads.
        with concurrent.futures.ThreadPoolExecutor() as pool:
            pool.map(self.download_files, post_list)

        
#####################################################################################################################################################


def main():
     # First try and load in the configuration file.
    config = rsConfig()

    # If no config could be parsed, then bail.
    if config.currentConfig == None:
        print("Generated Default Configuration File, Please fill in at least Credentials")
        exit()


    scraper = rsScraper(config)
    scraper.run()
   



if __name__ == "__main__":
    main()
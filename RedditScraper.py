#!/usr/bin/python

# Libraries
import praw
import requests
import re
import sys
import concurrent.futures
import os  
from urllib.parse import urlparse

# Local files
from rsConfig import rsConfig



def login_to_reddit(credentials: dict):

    try:
        # Attempt to login to reddit using the provided credential
        return praw.Reddit(     client_id=credentials['client_id'], 
                                client_secret=credentials['client_secret'], 
                                user_agent=credentials['user_agent'],
                                username=credentials['username'],
                                password=credentials['password'])
    except:
        return None
                       


def get_subscribed_subreddits(user, num: int):
    if num == 0:
        return list(user.subreddits())
    else:
        return list(user.subreddits(limit=num))



def filter_and_get_posts(posts, filters):

    found = 0
    curr_post = 0
    post_list = []

    for post in posts: 
        curr_post = curr_post + 1
        # Filter post
        if  not post.stickied \
            and post.over_18 == config.filters['allow_nsfw'] \
            and post.url.endswith(tuple(config.filters['white_list_file'])):

            # Create a tuple of URL and Filename and source subreddit for the post. Add to list.
            post_list.append( (os.path.basename(urlparse(post.url).path), post.url, subreddit.display_name) )
            found = found + 1

        # Once we have found enough valid posts or we reached max searches, exit loop
        if found >= config.runtime['default_entries'] or curr_post >= config.runtime['max_attempts'] :
            print(f'Found {found} files from {subreddit.display_name}')
            break

    return post_list



def download_files(postList, basePath, splitBySub, splitByDate):
    
    for post in post_list: 
        filename = post[0]
        # Now lets download the file
        req = requests.get(post[1])

        file_path = ''

        # If files are to be saved in separate Sub folders.
        if splitBySub:
            # Create the file path in sub folder. path = "'Base path' / 'configured output folder' / 'subreddit name' /"
            file_path = f'{base_path}/{post[2]}/'
        else:
            # Create the file path in base configured path. path = "'Base path' / 'configured output folder' /"
            file_path = f'{base_path}/'

        # Path does not exist, so lets create it.
        if not os.path.exists(file_path):
            os.mkdir(file_path)
            
        with open( file_path + filename, "wb" ) as f:
            f.write(req.content)

        
#####################################################################################################################################################


if __name__ == "__main__":

    # First try and load in the configuration file.
    config = rsConfig()

    # If no config could be parsed, then bail.
    if config.currentConfig == None:
        print("Generated Default Configuration File, Please fill in at least Credentials")
        exit()


    # Get the base path to save the files to. If it does not exist, create it.
    base_path = f'{os.getcwd()}/{config.output["output_folder"]}'
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    # Attempt to login into Reddit with the provided credentials.
    r = login_to_reddit(config.credentials)

    # Error Logging in, so bail
    if r == None:
       print("Unable to log into Reddit with the provided Credentials. Please Check the 'rsConfig.yml' config file!")
       exit()

    post_list = []

    # Get all the posts from the subreddits.
    for subreddit in get_subscribed_subreddits(r.user, config.runtime['limit_sr']):
        # Get the top posts of the day, and filter them based on config
        post_list = filter_and_get_posts(subreddit.hot(limit=None) , config.filters)      

    # Go through each post and download file
    download_files(post_list, base_path, config.output['separate_by_sub'], config.output['separate_by_date'])
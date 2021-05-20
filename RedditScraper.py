#!/usr/bin/python

import praw
import requests
import re
import sys
import pprint  
import yaml  
import io
import os  
from os import path 

# Define the default configuration structure.
default_config = {

    'credentials' : {
        'client_id' : '',
        'client_secret' : '',
        'user_agent' : '',
        'username' : '',
        'password' : ''
    },

    'run_time' : {
        'allow_nsfw': False,
        'default_entries' : 5,
        'use_user_subs' : True,  
        'limit_sr' : 0,
    },

    'output' : {
        'separate_by_sub': True,
        'output_folder' : 'Output/'
    },

    'black_list_src' : [],
    'white_list_src' : [],

    'black_list_sub' : [],
    'white_list_sub' : [],
    'additional_sub' : [],
}



def login_to_reddit(credentials):

    try:
        # Attempt to login to reddit using the provided credential
        reddit = praw.Reddit(   client_id=credentials['client_id'], 
                                client_secret=credentials['client_secret'], 
                                user_agent=credentials['user_agent'],
                                username=credentials['username'],
                                password=credentials['password'])
        return reddit
    except:
        return None
                       

def get_subscribed_subreddits(reddit):
    return list(reddit.user.subreddits(limit=5))          


def get_top_posts(reddit, subreddit, num_posts):     
    return reddit.subreddit(subreddit).hot(limit=num_posts)   


def get_filename_from_post(reddit, post):

    # If the post is hosted on reddit.
    if post.is_self == True:
        file_name = post.url.split("/")[-2] + ".jpg"
        print(file_name)   
        return file_name    
    else:
        url = (post.url)
        file_name = url.split("/")
        if len(file_name) == 0:
            file_name = re.findall("/(.*?)", url)
        file_name = file_name[-1]
        if "." not in file_name:
            file_name += ".jpg"
        print(file_name)
        return file_name


def load_config():

    # Check if the config does not exist.
    if path.exists('redditScraper.yml') != True:
        # Use the default config object to create the file.
        with io.open('redditScraper.yml', 'w', encoding='utf8') as outfile:
            yaml.dump(default_config, outfile, default_flow_style=False, allow_unicode=True)
        return default_config

    else:
        # File exists, so load it in.
        with io.open('redditScraper.yml', 'r') as input:
            return yaml.safe_load(input)
        
#####################################################################################################################################################


if __name__ == "__main__":

    # First try and load in the configuration file.
    config = load_config()

    # Can't do much with default config, so bail.
    if config == default_config:
        print("Generated Default Configuration File, Please fill in at least Credentials")
        exit()


    # Get the base path to save the files to. If it does not exist, create it.
    base_path = f'{os.getcwd()}/{config["output"]["output_folder"]}'
    if not path.exists(base_path):
        os.mkdir(base_path)

    # Attempt to login into Reddit with the provided credentials.
    r = login_to_reddit(config['credentials'])

    # Error Logging in, so bail
    if r == None:
       print("Unable to log into Reddit with the provided Credentials. Please Check the 'redditScraper.yml' config file!")
       exit()

    post_list = []

    # Get all the posts from the subreddits.
    for subreddit in get_subscribed_subreddits(r):
        # Get the top posts of the day.
        posts = get_top_posts(r, subreddit.display_name, config['run_time']['default_entries'])
        for post in posts: 
            # Create a tuple of URL and Filename and source subreddit for the post. Add to list.
            post_list.append( (get_filename_from_post(r, post), post.url, subreddit.display_name) )

    # Go through each post and download file
    for post in post_list: 
        filename = post[0]
        # Now lets download the file
        req = requests.get(post[1])

        file_path = ''

        # If files are to be saved in separate Sub folders.
        if config['output']['separate_by_sub']:
            # Create the file path in sub folder. path = "'Base path' / 'configured output folder' / 'subreddit name' /"
            file_path = f'{base_path}/{post[2]}/'
        else:
            # Create the file path in base configured path. path = "'Base path' / 'configured output folder' /"
            file_path = f'{base_path}/'

        # Path does not exist, so lets create it.
        if not path.exists(file_path):
            os.mkdir(file_path)
            
        with open( file_path + filename, "wb" ) as f:
            f.write(req.content)
            

        

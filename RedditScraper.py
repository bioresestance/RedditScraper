#!/usr/bin/python

import praw
import requests
import re
import sys
import pprint  
import pyyaml                 


def login_to_reddit(client_id, client_secret, user_agent, username, password):

    # Attempt to login to reddit using the provided credential
    return praw.Reddit( client_id=client_id, 
                        client_secret=client_secret, 
                        user_agent=user_agent,
                        username=username,
                        password=password)
                       

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


# def generate_default_config:

                       
                      
                     
#####################################################################################################################################################

if __name__ == "__main__":

    r = login_to_reddit(client_id='', 
                        client_secret='', 
                        user_agent='',
                        username='',
                        password='')

    subreddits = get_subscribed_subreddits(r)

    post_list = []

    # Loop through each of the retrieved subreddits to get all posts.
    for subreddit in subreddits:
        # Get the top posts of the day.
        posts = get_top_posts(r, subreddit.display_name, 5)
        for post in posts: post_list.append(post)
        for post in post_list: 
            filename = get_filename_from_post(r, post)
            # Now lets download the file
            req = requests.get(post.url)
            with open( "Output/" + filename,"wb") as f:
                f.write(req.content)
            

        

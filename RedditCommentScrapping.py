#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 09:03:21 2023

reddit Scrapper    

@author: Karol Paczocha
"""

import praw
import pandas as pd
import re
########################### Missing fatures ###################################
##the url needs to be looped by the urls of the subreddits DF
##
##################### Setting up initial parameters############################
#to set up a reddit app please use https://old.reddit.com/prefs/apps/

clientId = "p8o293eNpz2fmKD2qdQcZg"
clientSecret = "ZDu6ijOQd_JxnQRZhn6xiFSOU4r1tw"
userAgent = "UWL webscrapping"
username = "*****"#for obvious reasons the login and password are not included
password = "*****"

#Create a dictonary that will store the posts information
postsDictionary = {"Title": [],
                    "Post Text": [],
                    "ID": [],
                    "Score": [],
                    "Total Comments": [],
                    "Post URL": []}
# Read-only instance
redditReadOnly = praw.Reddit(  client_id= clientId,         
                               client_secret= clientSecret,      
                               user_agent = userAgent)        
# Authorized instance
redditAuthorized = praw.Reddit(client_id= clientId,        
                                client_secret= clientSecret,     
                                user_agent= userAgent,     
                                username= username,       
                                password= password)
###############################################################################
#############################Setting up extraction#############################
#Subredit used for scrapping
subreddit = redditReadOnly.subreddit("ChiariMalformation")##only the name of the subreddit is needed not the whole link


#print basic information about a subreddit to see if it loads
print("name: ", subreddit.display_name)
print("title: ", subreddit.title)
print("description: ", subreddit.description)

##Loop for a each post for a subreddit in a category

condition = "year" ##use the current month as the condition more cna be found on the documentation this is just an example 
posts = subreddit.top(condition)

for post in posts:
    # Title of each post
    postsDictionary["Title"].append(post.title)
     
    # Text inside a post
    postsDictionary["Post Text"].append(post.selftext)
     
    # Unique ID of each post
    postsDictionary["ID"].append(post.id)
     
    # The score of a post
    postsDictionary["Score"].append(post.score)
     
    # Total number of comments inside the post
    postsDictionary["Total Comments"].append(post.num_comments)
     
    # URL of each post
    postsDictionary["Post URL"].append(post.url)
###############################################################################
#Create a pandas dataframe for posts on the subreddit
postsData = pd.DataFrame(postsDictionary)
postsData.to_csv("Reddit_WS.csv", index = False)

##Url of the post (will be extracted from the pd dataframe in the future)
#url2 = "https://www.reddit.com/r/Python/comments/15h05rm/polars_is_starting_a_company/"

url_list = []


def get_url():
    for url in postsData['Post URL']:
        m = re.search(r'(?<=\.)([^.]+)(?:\.(?:co[^.]))', url)
        if m:
            if m.group() == "reddit.com":
                url_list.append(url)
                get_comments(url)


#Submition object
    

#Scrapping for all the comments under the post
postComments = []

#Getting comments using the praws morecomments function
def get_comments(url):
    submission = redditReadOnly.submission(url=url)
    for comment in submission.comments:
        if type(comment) == praw.models.MoreComments: #Check for the type if it mateches continue to the next comment under the post
         continue
        postComments.append(comment.body)#getting only the content of the commredditReadOnlyent
        
        
get_url()        
    
#Create a dataframe for the extracted comments
commentsData = pd.DataFrame(postComments, columns = ["Post Comment"])
commentsData.to_csv("commentsdata.csv", index = False)
    

##Using this layout the code can be manipulated to obtain much more information!
##I have only followed the basic documentation by praw to help set up this code to work
##Some features will still need to be implemented
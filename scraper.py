#!/usr/bin/python3
# File name: scraper.py
# Script for collecting comments from the subreddit r/thenetherlands, sorted by 'Controversial' and 'All time'.
# Author: Zhenja Gnezdilov

import praw
import pandas as pd


def scraper():
    posts = []
    comment_counter, post_counter = 0, 0
    reddit = praw.Reddit(client_id="zLshLecXEZYfnQ",
                         client_secret="0H1mnEvZojcWHwvTwKHQAVccdSf0qg",
                         user_agent="Comment WebScraping")

    # get all comments from every post in r/thenetherlands, sorted by 'controversial' and 'all time'
    for submission in reddit.subreddit("thenetherlands").controversial():
        post = reddit.submission(id=submission.id)
        post_counter += 1

        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            # exclude deleted and removed comments
            if comment.body == "[deleted]" or comment.body == "[removed]":
                continue
            comment_counter += 1
            posts.append([post.id, comment.body, ""])
        # get around 500 comments
        if comment_counter >= 500:
            break
    print(f"Got {comment_counter} comments in total. The comments were taken from {post_counter} posts.")
    print("Saving them to a .csv file...\n")
    df = pd.DataFrame(posts, columns=["post id", "text", "explicitness"])
    df.to_csv("reddit_comments.csv", index=False, encoding="utf-8", na_rep="")


def main():
    print("Starting collection of Reddit comments on r/thenetherlands, sorted by 'Controversial' and 'All time'...\n")
    scraper()
    print("All done! See reddit_comments.csv for the results.")


if __name__ == "__main__":
    main()

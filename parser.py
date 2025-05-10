import requests
from bs4 import BeautifulSoup
import time
import sqlite3

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
delay = 3


def get_posts(subreddits, start_date="none"):
    posts = []
    for subreddit in subreddits:
        subreddit_link = f"https://old.reddit.com/r/{subreddit}/new/"
        while True:
            exit_flag = False
            web_content = requests.get(subreddit_link, verify=False, headers=headers)
            web_content_soup = BeautifulSoup(web_content.text, "html.parser")
            posts_containers = web_content_soup.find_all("div", class_="top-matter")
            if len(posts_containers) < 25: 
                exit_flag = True
            for post in posts_containers:
                post_id, post_title = post.find("a", {"data-event-action": "comments"})['href'].replace(f"https://old.reddit.com/r/{subreddit}/comments/", "").strip("/").split("/")
                post_timestamp = post.find("time", class_="live-timestamp")['datetime']
                if post_timestamp <= start_date:
                    exit_flag = True
                    break
                posts.append({'subreddit': subreddit,
                              'post_id': post_id,
                              'post_title': post_title,
                              'post_timestamp': post_timestamp})
            if exit_flag == True:
                break
            subreddit_link = f"https://old.reddit.com/r/{subreddit}/new/?count=25&after=t3_{post_id}"
            time.sleep(delay)
    return posts


def get_text_from_posts(posts):
    for post in posts:
        post_link = f"https://www.reddit.com/r/{post['subreddit']}/comments/{post['post_id']}/{post['post_title']}/"
        web_content = requests.get(post_link, verify=False, headers=headers)
        web_content_soup = BeautifulSoup(web_content.text, "html.parser")
        post_content = web_content_soup.find("div", class_="md max-h-[253px] overflow-hidden s:max-h-[318px] m:max-h-[337px] l:max-h-[352px] xl:max-h-[452px] text-14")
        try:
            post['post_text'] = post_content.text
        except:
            post['post_text'] = "No content"
        time.sleep(delay)
    return posts


def writre_to_db(posts, db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    try:
        cursor.executemany("INSERT INTO posts (subreddit, post_id, post_title, post_timestamp, post_text) VALUES(:subreddit, :post_id, :post_title, :post_timestamp, :post_text)", posts)
    except:
        cursor.execute('CREATE TABLE posts(subreddit, post_id, post_title, post_timestamp, post_text)')
        cursor.executemany("INSERT INTO posts (subreddit, post_id, post_title, post_timestamp, post_text) VALUES(:subreddit, :post_id, :post_title, :post_timestamp, :post_text)", posts)
    connection.commit()



posts = get_posts(['AIJailbreak', 'ChatGPTJailbreak', 'ChatGptDAN', 'GPT_jailbreaks', 'OnlyJailbreaks', 'maximumai'], start_date="2025-04-01T00:00:01+00:00")
post_text = get_text_from_posts(posts)
writre_to_db(post_text, "db/db1.db")
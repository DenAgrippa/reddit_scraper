import requests
from bs4 import BeautifulSoup

def get_posts_ids(subreddit_names, start_date, end_date="current"):
    pass

def get_text_from_posts(post_ids):
    for subreddit, post_id in post_ids:
        post_link = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}/"
        web_content = requests.get(post_link)
        web_content_soup = BeautifulSoup(web_content.text, "html.parser")
        post = web_content_soup.find("div")
    return post.text

def writre_to_db(posts, db):
    pass

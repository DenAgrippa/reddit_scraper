import requests
from bs4 import BeautifulSoup

def get_posts(subreddits, start_date, end_date="current"):
    posts = []
    for subreddit in subreddits:
        subreddit_link = f"https://www.old.reddit.com/r/{subreddit}/new/"
        web_content = requests.get(subreddit_link)
        web_content_soup = BeautifulSoup(web_content.text, "html.parser")
        posts_containers = web_content_soup.find_all("div", class_='top-matter')


def get_text_from_posts(post):
    post_link = f"https://www.reddit.com/r/{post['subreddit']}/comments/{post['post_id']}/{post['title']}/"
    web_content = requests.get(post_link)
    web_content_soup = BeautifulSoup(web_content.text, "html.parser")
    post = web_content_soup.find("div", class_="md max-h-[253px] overflow-hidden s:max-h-[318px] m:max-h-[337px] l:max-h-[352px] xl:max-h-[452px] text-14")
    return post.get_text()

def writre_to_db(posts, db):
    pass

""" posts = [{'subreddit': 'ChatGPTJailbreak',
            'post_id': '1keo6xf',
            'title': 'why_do_every_ai_thinks_819_mod_26_is_15_chatgpt'}]

subreddits = ['ChatGPTJailbreak', 'Qwen_AI']

for post in posts:
    print(get_text_from_posts(post)) """
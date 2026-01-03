import requests
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def fetch_page(url):
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html

def write_posts_to_file(posts:list, filename):
    """Write the list of posts to a text file as json."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump([post.__dict__ for post in posts], file, ensure_ascii=False, indent=4)



class Post:
    """A class representing a blog post."""

    def __init__(self, title, author_name, date, text):
        self.title = title
        self.author_name = author_name
        self.date = date
        self.text = text


def extract_posts(html):
    # this is the main relevant function to implement
    pass
    
if __name__ == "__main__":
    url = 'https://www.phpbb.com/community/viewtopic.php?p=13166053#p13166053'
    url = 'https://forum.vbulletin.com/forum/vbulletin-3-8/vbulletin-3-8-questions-problems-and-troubleshooting/414325-www-vs-non-www-url-causing-site-not-to-login'
    html_content = fetch_page(url)

    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(html_content) # this will be removed later

    posts = extract_posts(html_content)
    # write_posts_to_file(posts, 'posts.json')
    # print(f"Extracted {len(posts)} posts.")
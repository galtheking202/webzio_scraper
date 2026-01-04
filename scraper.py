import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import * 

def fetch_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html


def extract_posts_bulletin(html):
    authors = extract_by_class_or_id(html, class_name="author h-text-size--14")
    contents = extract_by_class_or_id(html, class_name="OLD__post-content h-padding-vert-xl")
    titles_and_dates = extract_by_class_or_id(html, class_name="b-media__body") # same div

    titles,publish_datetimes = [],[]
    for tnd in titles_and_dates: # this will split the time and date
        title_and_date_list = tnd.splitlines()
        if len(title_and_date_list) > 1:
            titles.append(title_and_date_list[0])
            publish_datetimes.append(normalize_datetime(title_and_date_list[1],BUILLETIN_DATETIME_FORMAT))
        else:
            titles.append("No Title")
            publish_datetimes.append(normalize_datetime(title_and_date_list[0],BUILLETIN_DATETIME_FORMAT))
    return lists_to_posts(titles,authors,publish_datetimes,contents)
    

def extract_posts_phpp(html):
    authors_and_publish_datetimes_container = extract_by_class_or_id(html, tag='p',class_name="author") # date and username container
    contents = extract_by_class_or_id(html,class_name="content")
    title_containers = extract_by_class_or_id(html,class_name="postbody") # title container

    authors,publish_datetimes = [],[]
    for aad in authors_and_publish_datetimes_container: # extract datetimes and authors from the same container
        publish_datetimes.append(normalize_datetime(aad.split(" » ")[1],PPHP_DATETIME_FORMAT))
        authors.append(re.search(r"by(.*?) » ",aad).group(1).strip())

    titles = [title_container.split("\nQuote")[0] for title_container in title_containers] # extract title from its container.

    return lists_to_posts(titles,authors,publish_datetimes,contents)



if __name__ == "__main__":
    phpbb = 'https://www.phpbb.com/community/viewtopic.php?p=13166053#p13166053'
    bulletin = 'https://forum.vbulletin.com/forum/vbulletin-3-8/vbulletin-3-8-questions-problems-and-troubleshooting/414325-www-vs-non-www-url-causing-site-not-to-login'

    html_content_bulletin = fetch_page(bulletin)
    html_content_phpbb = fetch_page(phpbb)

    posts = extract_posts_phpp(html_content_phpbb)
    write_posts_to_file(posts, 'phpbb.json')
    print(f"Extracted {len(posts)} posts.")

    posts = extract_posts_bulletin(html_content_bulletin)
    write_posts_to_file(posts, 'bulletin.json')
    print(f"Extracted {len(posts)} posts.")
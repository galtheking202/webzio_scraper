import re
import json
from datetime import datetime

PPHP_DATETIME_FORMAT = "%a %b %d, %Y %I:%M %p"
BUILLETIN_DATETIME_FORMAT = "%a %d %b '%y, %I:%M%p"
STANDARD_DATETIME_FORMAT = "%Y/%m/%d %H:%M"

class Post:
    """A class representing a blog post."""

    def __init__(self, title, author, published, text):
        self.title = title
        self.text = text
        self.published = published
        self.author = author


def extract_by_class_or_id(
    html: str, 
    tag: str = "div", 
    class_name: str = None, 
    id_name: str = None, 
    remove_html: bool = True
) -> list:
    """
    Extracts inner content of a specified HTML tag by class or id, handling nested tags.
    
    Parameters:
        html (str): HTML text to search.
        tag (str): HTML tag to extract (e.g., 'div', 'p', 'span').
        class_name (str): Class name of the tag to extract.
        id_name (str): ID of the tag to extract.
        remove_html (bool): Whether to remove inner HTML tags from the result.

    Returns:
        List[str]: List of inner text (or HTML if remove_html=False) of all matching tags.
    """
    if not class_name and not id_name:
        raise ValueError("Either class_name or id_name must be provided.")
    
    # Build regex to find opening tags
    if class_name:
        open_tag_pattern = re.compile(
            rf'<{tag}[^>]*class=["\']{re.escape(class_name)}["\'][^>]*>', 
            re.IGNORECASE
        )
    else:
        open_tag_pattern = re.compile(
            rf'<{tag}[^>]*id=["\']{re.escape(id_name)}["\'][^>]*>', 
            re.IGNORECASE
        )
    
    results = []
    
    for match in open_tag_pattern.finditer(html):
        idx = match.end()
        count = 1  # opening tag found

        # Scan forward manually to handle nested tags of the same type
        while idx < len(html) and count > 0:
            # check for next opening tag
            open_match = re.match(rf'<{tag}[^>]*>', html[idx:], re.IGNORECASE)
            close_match = re.match(rf'</{tag}>', html[idx:], re.IGNORECASE)

            if open_match:
                count += 1
                idx += open_match.end()
            elif close_match:
                count -= 1
                idx += close_match.end()
            else:
                print(idx)
                idx += 1

        # Extract inner HTML
        inner_html = html[match.end():idx - len(f'</{tag}>')]

        # Clean HTML if needed
        if remove_html:
            inner_html = re.sub(r'<br\s*/?>', '\n', inner_html, flags=re.IGNORECASE)
            inner_html = re.sub(r'<[^>]+>', '', inner_html)
            inner_html = re.sub(r'\t', '', inner_html)
            inner_html = re.sub(r'\n\s*\n', '\n', inner_html)  # remove empty lines
            inner_html = inner_html.strip()

        results.append(inner_html)

    return results


def write_posts_to_file(posts:list, filename):
    """Write the list of posts to a text file as json."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump([post.__dict__ for post in posts], file, ensure_ascii=False, indent=4)


def normalize_datetime(time_str,old_format,new_format=STANDARD_DATETIME_FORMAT):
    return datetime.strptime(time_str, old_format).strftime(new_format)
    

def lists_to_posts(titles,authors,publish_datetimes,contents):
    assert len(titles)==len(authors)==len(publish_datetimes)==len(contents), "Something went wrong, some data is missing..."

    return [Post(titles[i],authors[i],publish_datetimes[i],contents[i]) for i in range(len(titles))]
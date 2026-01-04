import re

def extract_div_content(html: str, div_class: str = None, div_id: str = None) -> list:
    """
    Extracts inner content of <div> by class or id.

    Parameters:
        html (str): HTML text to search.
        div_class (str): Class name of the div to extract.
        div_id (str): ID of the div to extract.

    Returns:
        List[str]: A list of inner HTML/text of all matching divs.
    """
    
    if not div_class and not div_id:
        raise ValueError("Either div_class or div_id must be provided.")
    
    if div_class:
        # Match div by class
        pattern = rf'<div[^>]*class=["\']{re.escape(div_class)}["\'][^>]*>(.*?)</div>'
    else:
        # Match div by id
        pattern = rf'<div[^>]*id=["\']{re.escape(div_id)}["\'][^>]*>(.*?)</div>'
    
    # re.DOTALL allows matching multiline HTML
    matches = re.findall(pattern, html, re.DOTALL)
    
    # Optional: strip leading/trailing spaces from each match
    matches = [m.strip() for m in matches]
    
    return matches

import re

def extract_div_text(html: str, div_class: str = None, div_id: str = None) -> list:
    """
    Extracts inner text of <div> by class or id, removing all HTML tags.

    Parameters:
        html (str): HTML text to search.
        div_class (str): Class name of the div to extract.
        div_id (str): ID of the div to extract.

    Returns:
        List[str]: A list of clean text of all matching divs.
    """
    if not div_class and not div_id:
        raise ValueError("Either div_class or div_id must be provided.")

    # Match div by class or id
    if div_class:
        pattern = rf'<div[^>]*class=["\']{re.escape(div_class)}["\'][^>]*>(.*?)</div>'
    else:
        pattern = rf'<div[^>]*id=["\']{re.escape(div_id)}["\'][^>]*>(.*?)</div>'
    
    # Get all inner HTML matches
    matches = re.findall(pattern, html, re.DOTALL)

    clean_texts = []
    for m in matches:
        # Replace <br> or <br /> with newlines
        text = re.sub(r'<br\s*/?>', '\n', m, flags=re.IGNORECASE)
        # Remove all remaining HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Replace multiple spaces/newlines with single space/newline
        text = re.sub(r'\n\s*\n', '\n', text)  # remove empty lines
        text = text.strip()
        clean_texts.append(text)
    
    return clean_texts

def extract_nested_div(html, div_class):
    start = html.find(f'class="{div_class}"')
    if start == -1:
        return None
    start = html.rfind('<div', 0, start)  # start of opening div

    count = 0
    end = start
    while end < len(html):
        if html[end:end+4] == '<div':
            count += 1
        elif html[end:end+5] == '</div':
            count -= 1
            if count == 0:
                end += 6  # include closing </div>
                break
        end += 1
    return html[start:end]

import re

def h3_extract_title(html: str) -> list:
    print(html)
    match = re.search(r'<h3[^>]*>\s*<a[^>]*>\s*(.*?)\s*</a>', html, re.DOTALL)
    if match:
        title = match.group(1).strip()
    return title

def extract_nested_div(html: str, div_class: str = None, div_id: str = None, remove_html: bool = True) -> list:
    """
    Extracts inner text of <div> by class or id, handling nested divs.
    
    Parameters:
        html (str): HTML text to search.
        div_class (str): Class name of the div to extract.
        div_id (str): ID of the div to extract.

    Returns:
        List[str]: List of inner text (with HTML removed) of all matching divs.
    """
    if not div_class and not div_id:
        raise ValueError("Either div_class or div_id must be provided.")

    # Build regex to find opening divs
    if div_class:
        open_div_pattern = re.compile(rf'<div[^>]*class=["\']{re.escape(div_class)}["\'][^>]*>', re.IGNORECASE)
    else:
        open_div_pattern = re.compile(rf'<div[^>]*id=["\']{re.escape(div_id)}["\'][^>]*>', re.IGNORECASE)

    results = []
    for match in open_div_pattern.finditer(html):
        start_idx = match.start()
        idx = match.end()
        count = 1  # opening div found

        # scan forward manually
        while idx < len(html) and count > 0:
            # check for next opening div
            open_match = re.match(r'<div[^>]*>', html[idx:], re.IGNORECASE)
            close_match = re.match(r'</div>', html[idx:], re.IGNORECASE)

            if open_match:
                count += 1
                idx += open_match.end()
            elif close_match:
                count -= 1
                idx += close_match.end()
            else:
                idx += 1

        text = html[match.end():idx - 6]  # exclude last </div>

        # Clean inner HTML
        if remove_html:
            text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
            text = re.sub(r'<[^>]+>', '', text)
            text = re.sub(r'\t','',text)
            text = re.sub(r'\n\s*\n', '\n', text)  # remove empty lines
            text = text.strip()
        results.append(text)

    return results

if __name__ == "__main__":
    with open("output2.html", "r", encoding="utf-8") as f:
        file_content = f.read()
    divs_by_class = extract_nested_div(file_content, div_class="author h-text-size--14")
    divs_by_class = extract_nested_div(file_content, div_class="b-post__timestamp")
    divs_by_class = extract_nested_div(file_content, div_class="OLD__post-content h-padding-vert-xl")
    divs_by_class = extract_nested_div(file_content, div_class="b-media__body")
    print(divs_by_class[0].splitlines())
    # print(f"Found {len(divs_by_class)} divs with class 'b-post__grid-container':")
    # for i, div in enumerate(divs_by_class, 1):  # start enumeration at 1
        # print(f"\n--- Div {i} ---\n{div}\n")    
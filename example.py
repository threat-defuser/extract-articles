from tqdm import tqdm
import justext
import requests
from lxml import etree
from datetime import datetime
import hashlib
from google.cloud import firestore


def extract_text(url: str, language: str) -> (list[str], str):
    headings = []
    paragraphs = []
    response = requests.get(url)
    page = response.text.encode("utf-8")
    for paragraph in justext.justext(page, justext.get_stoplist(language)):
        if paragraph.class_type == "good":
            if paragraph.heading:
                headings.append(paragraph.text)
            paragraphs.append(paragraph.text)
    # returning response.url since url might be redirected
    return response.url, headings, "\n".join(paragraphs)


def test_extract_test():
    url = "https://w.wiki/U"
    language = "English"
    final_url, headings, text = extract_text(url, language)
    assert final_url == "https://en.wikipedia.org/wiki/URL_shortening"
    assert "URL shortening is a technique on the World Wide Web" in text


def get_timestamp() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def get_urls(sitemap: str) -> list[str]:
    urls = []
    r = requests.get(sitemap)
    root = etree.fromstring(r.content)
    for sitemap in root:
        children = sitemap.getchildren()
        if len(children) == 2:
            url = children[0].text
            if "utenriks" in url:  # FIXME
                urls.append(url)
    return urls


def print_data(url: str, language: str):
    _, headings, text = extract_text(url, language)
    timestamp = get_timestamp()
    document_id = hash_url(url)
    print(f"\nheadings: {headings}")
    print(f"\ntext: {text}")
    print(f"\ntimestamp: {timestamp}")
    print(f"\ndocument_id: {document_id}")


def extract_and_write_to_db(url: str, language: str):
    _, headings, text = extract_text(url, language)
    timestamp = get_timestamp()
    document_id = hash_url(url)

    db = firestore.Client()

    doc_ref = db.collection("articles").document(document_id)
    doc_ref.set({"timestamp": timestamp, "headings": headings, "text": text})


if __name__ == "__main__":
    urls = get_urls("https://www.lykten.no/sitemap.xml")
    language = "Norwegian_Bokmal"
    for url in tqdm(urls):
        # extract_and_write_to_db(url, language)
        print_data(url, language)

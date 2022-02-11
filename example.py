from tqdm import tqdm
import justext
import time
import requests
from lxml import etree
from datetime import datetime
import hashlib
from google.cloud import firestore
from bs4 import BeautifulSoup


def extract_text(url: str, language: str, session) -> (list[str], str):
    headings = []
    paragraphs = []
    t0 = time.time()
    response = session.get(url)
    html = response.text.encode("utf-8")
    print("time spent in requests:", time.time() - t0)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")

    t0 = time.time()
    for paragraph in justext.justext(html, justext.get_stoplist(language)):
        if paragraph.class_type == "good":
            if paragraph.heading:
                headings.append(paragraph.text)
            paragraphs.append(paragraph.text)
    print("time spent in justext:", time.time() - t0)

    # returning response.url since url might be redirected
    return response.url, title.string, headings, "\n".join(paragraphs), html


def test_extract_test():
    url = "https://w.wiki/U"
    language = "English"
    session = requests.Session()
    final_url, title, headings, text, html = extract_text(url, language, session)
    assert final_url == "https://en.wikipedia.org/wiki/URL_shortening"
    assert "URL shortening is a technique on the World Wide Web" in text


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


def extract_and_write_to_db(url: str, language: str, session):
    final_url, title, headings, text, html = extract_text(url, language, session)
    unix_time = int(time.time())
    document_id = f"{hash_url(url)}-{unix_time}"

    d = {}
    d["url"] = final_url
    d["timestamp"] = unix_time
    d["title"] = title
    d["headings"] = headings
    d["text"] = text
    d["html"] = html

    db = firestore.Client()
    doc_ref = db.collection("articles").document(document_id)
    doc_ref.set(d)


if __name__ == "__main__":
    urls = get_urls("https://www.lykten.no/sitemap.xml")
    language = "Norwegian_Bokmal"
    session = requests.Session()
    for url in tqdm(urls):
        extract_and_write_to_db(url, language, session)

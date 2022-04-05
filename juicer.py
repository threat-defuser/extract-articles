import justext
import requests
from bs4 import BeautifulSoup


def extract(url: str, language: str, session) -> (list[str], str):
    headings = []
    paragraphs = []
    # t0 = time.time()
    response = session.get(url)
    html = response.text.encode("utf-8")
    # print("time spent in requests:", time.time() - t0)
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")

    # t0 = time.time()
    for paragraph in justext.justext(html, justext.get_stoplist(language)):
        if paragraph.class_type == "good":
            if paragraph.heading:
                headings.append(paragraph.text)
            paragraphs.append(paragraph.text)
    # print("time spent in justext:", time.time() - t0)

    # returning response.url since url might be redirected
    return response.url, title.string, headings, "\n".join(paragraphs), html


def test_extract():
    url = "https://w.wiki/U"
    language = "English"
    session = requests.Session()
    final_url, title, headings, text, html = extract(url, language, session)
    assert final_url == "https://en.wikipedia.org/wiki/URL_shortening"
    assert "URL shortening is a technique on the World Wide Web" in text

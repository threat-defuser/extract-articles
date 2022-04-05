import requests

from extract_plaintext import extract
from db import make_sure_table_exists, save_entry, read_entries


def extract_and_save(db_file_name: str, url_language_tuples: tuple[str, str]):
    make_sure_table_exists(db_file_name)
    session = requests.Session()
    for (url, language) in url_language_tuples:
        final_url, title, _headings, text, html = extract(url, language, session)
        save_entry(db_file_name, final_url, title, text, html)


def test_extract_and_save():
    db_file_name = "articles.db"
    url_language_tuples = [("https://w.wiki/U", "English")]
    extract_and_save(db_file_name, url_language_tuples)
    rows = read_entries(db_file_name)

import requests
import click
from tqdm import tqdm
import csv

from extract_plaintext import extract
from db import make_sure_table_exists, save_entry, read_entries


def extract_and_save(db_file_name: str, url_language_tuples: tuple[str, str]):
    make_sure_table_exists(db_file_name)
    session = requests.Session()
    for (url, language) in tqdm(url_language_tuples):
        final_url, title, _headings, text, html = extract(url, language, session)
        save_entry(db_file_name, final_url, title, text, html)


def test_extract_and_save():
    db_file_name = "articles.db"
    url_language_tuples = [("https://w.wiki/U", "English")]
    extract_and_save(db_file_name, url_language_tuples)
    _rows = read_entries(db_file_name)


def _hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


@click.command()
@click.option(
    "--csv-file", help="The input CSV file containing list of URLs to process."
)
@click.option("--db-file", help="The SQLite database file.")
def main(csv_file, db_file):
    urls = []
    languages = []
    with open(csv_file) as f:
        for row in csv.DictReader(f):
            urls.append(row["url"])
            languages.append(row["language"])
    url_language_tuples = list(zip(urls, languages))
    extract_and_save(db_file, url_language_tuples)


if __name__ == "__main__":
    main()

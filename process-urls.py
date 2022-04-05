import requests
import click
from tqdm import tqdm
import csv

from juicer import extract
from db import make_sure_table_exists, save_entry, read_entries


def extract_and_save(db_file_name: str, pages: tuple[str, str, str]):
    make_sure_table_exists(db_file_name)
    session = requests.Session()
    for (site_name, url, language) in tqdm(pages):
        final_url, title, _headings, text, html = extract(url, language, session)
        save_entry(db_file_name, site_name, final_url, title, text, html)


def test_extract_and_save():
    db_file_name = "articles.db"
    pages = [("Example site", "https://w.wiki/U", "English")]
    extract_and_save(db_file_name, pages)
    _rows = read_entries(db_file_name)


def _hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


@click.command()
@click.option(
    "--csv-file",
    required=True,
    help="The input CSV file containing list of URLs to process.",
)
@click.option("--db-file", required=True, help="The SQLite database file.")
def main(csv_file, db_file):
    site_names = []
    urls = []
    languages = []
    with open(csv_file) as f:
        for row in csv.DictReader(f):
            site_names.append(row["name"])
            urls.append(row["url"])
            languages.append(row["language"])
    pages = list(zip(site_names, urls, languages))
    extract_and_save(db_file, pages)


if __name__ == "__main__":
    main()

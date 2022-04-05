import requests
from lxml import etree
import re
import click
import yaml
import sys
import csv


def get_urls(sitemap: str) -> list[str]:
    urls = []
    r = requests.get(sitemap)
    root = etree.fromstring(r.content)
    for sitemap in root:
        children = sitemap.getchildren()
        if len(children) == 2:
            url = children[0].text
            urls.append(url)
    return urls


def extract_data(file_name: str):
    with open(file_name, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            sys.exit(e)
    return data


@click.command()
@click.option(
    "--sites", help="The YML file describing the sites. This file is only read."
)
@click.option("--out-file", help="The generated output CSV file.")
def main(sites, out_file):
    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "language"])
        for site in extract_data(sites):
            urls = get_urls(site["url"])
            regex_objects = [re.compile(pattern) for pattern in site["include"]]
            for url in urls:
                for regex in regex_objects:
                    if regex.search(url):
                        writer.writerow([url, site["language"]])
                        break


if __name__ == "__main__":
    main()

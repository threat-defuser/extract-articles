import requests
from lxml import etree
import re
import click
import yaml
import sys
import csv
import tldextract


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


def extract_sites(file_name: str):
    with open(file_name, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            sys.exit(e)
    return data


def filter_urls(urls, include_patterns):
    regex_objects = [re.compile(pattern) for pattern in include_patterns]
    matching_urls = []
    for url in urls:
        for regex in regex_objects:
            if regex.search(url):
                matching_urls.append(url)
                break
    return matching_urls


def extract_tld(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"


@click.command()
@click.option(
    "--sites",
    required=True,
    help="The YML file describing the sites. This file is only read.",
)
@click.option("--out-file", required=True, help="The generated output CSV file.")
@click.option(
    "--pages-per-site",
    type=int,
    help="Sample only so many pages per site for testing purposes [default: collect all pages].",
)
def main(sites, out_file, pages_per_site):

    if pages_per_site is None:
        pages_per_site = sys.maxsize

    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "url", "language"])
        for site in extract_sites(sites):
            site_tld = extract_tld(site["url"])
            urls = get_urls(site["url"])
            if "include" in site:
                urls = filter_urls(urls, site["include"])
            for url in urls[:pages_per_site]:
                tld = extract_tld(url)
                if tld == site_tld:
                    writer.writerow([site["name"], url, site["language"]])


if __name__ == "__main__":
    main()

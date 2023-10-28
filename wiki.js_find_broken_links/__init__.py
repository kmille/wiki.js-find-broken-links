import sys
import argparse
from pathlib import Path
import requests
import re
import browser_cookie3
from bs4 import BeautifulSoup
import logging

DEFAULT_FILTER = "public/CRM"
DEFAULT_WIKI_CONTENT = Path("/home/kmille/projects/evil-corp/wiki-content")

BASE_URL = "https://wiki.evil-corp.com"

session = requests.Session()
session.headers.update({'User-Agent': 'Firefox'})

FORMAT = "[%(levelname)7s] %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=FORMAT)


def check_page(file: Path, url: str):
    if "@" in url or "tel:" in url or "google." in url or "youtube." in url or "youtu.be" in url:
        return
    if url.startswith("/"):
        url = BASE_URL + url
    logging.debug(f"   Checking {url}")
    try:
        resp = session.get(url)
        resp.raise_for_status()
        logging.debug("   Link OK")
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema) as oh:
        logging.warning(f"Found invalid link in {file}: {oh}")
    except requests.exceptions.HTTPError as e:
        logging.warning(f"Broken Link in file {file.resolve()}: {e}")


def iterate_over_wikijs_backup(wiki_filter: str, wiki_content: str):
    for p in wiki_content.rglob("*"):
        if not p.is_file():
            continue
        if wiki_filter not in str(p.resolve()):
            continue
        if p.suffix not in (".md", ".html"):
            continue
        logging.debug(f"Processing {p}")
        text = p.read_text()
        if p.suffix == ".md":
            links = re.findall(r"(?:\[(?P<text>.*?)\])\((?P<link>.*?)\)", text)
        if p.suffix == ".html":
            bs = BeautifulSoup(text, 'html.parser')
            links = []
            for a in bs.find_all("a"):
                links.append((a.text, a.attrs["href"]))
        for link in links:
            desc, url = link
            logging.debug(f" Found link to '{desc}': {url}")
            check_page(p, url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="show verbose output", action="store_true")
    parser.add_argument("-f", "--wiki-filter", help="filter for wiki pages", default=DEFAULT_FILTER)
    parser.add_argument("-l", "--login", help="use browser cookies for login", action="store_true")
    parser.add_argument("-w", "--wiki-content", help="location of wikijs backup directory", default=DEFAULT_WIKI_CONTENT)

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)

    if args.login:
        browser_cookies = browser_cookie3.load()
        session.cookies.update(browser_cookies)
        logging.info("Using browser cookies")

    try:
        logging.info(f"Using wiki filter: {args.wiki_filter} (only using wiki pages containing this string)")
        logging.info(f"Using wiki content directory: {args.wiki_content}")
        logging.info(f"Please update the backup git repo before executing this script: git -C {args.wiki_content} pull")
        iterate_over_wikijs_backup(args.wiki_filter, args.wiki_content)
    except KeyboardInterrupt:
        sys.exit(0)

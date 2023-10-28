# A simple tool to find broken links in wiki.js

Needs:
- location of wiki.js backup directory (a directory which clones git@git.evil-corp.com:infra/wiki-content)
- optional: a filter like 'intern' or public/CRM (will be compared to the file names)
- login: it can use your browser cookies (to test internal wiki pages)
- verbose: for a more verbose output

Outputs: HTTP errors (40x, 50x)

## How to use it
You need poetry. Use `git clone`, then `poetry install`. Then you can run `poetry run python wiki.js_find_broken_links/__init__.py -h`


```bash
kmille@linbox:wikjs-broken-links poetry run python wiki.js_find_broken_links/__init__.py -h                    
usage: __init__.py [-h] [-v] [-f WIKI_FILTER] [-l] [-w WIKI_CONTENT]

options:
  -h, --help            show this help message and exit
  -v, --verbose         show verbose output
  -f WIKI_FILTER, --wiki-filter WIKI_FILTER
                        filter for wiki pages
  -l, --login           use browser cookies for login
  -w WIKI_CONTENT, --wiki-content WIKI_CONTENT
                        location of wikijs backup directory
```

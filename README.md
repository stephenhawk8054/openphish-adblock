# openphish-adblock
Openphish feed in adblock syntaxes

The filter list is curated from [OpenPhish](https://openphish.com/). The URL feed is fetched from [OpenPhish Community Phishing Feed](https://openphish.com/phishing_feeds.html) at least twice a day. Compatible with uBlock Origin and Adguard.

## Links for adding to blocker extensions

- URL path version: https://cdn.jsdelivr.net/gh/stephenhawk8054/openphish-adblock@latest/filters.txt
- Domain version: https://cdn.jsdelivr.net/gh/stephenhawk8054/openphish-adblock@latest/filters_domains.txt

## Some modifications comparing to original feeds

- Ignore queries (`?`, `&`) and fragments (`#`) in the URLs,
- Ignore `www.` at the start of the domains,
- If a URL matches one of the URL/domain paths in [`domain_paths.txt`](https://github.com/stephenhawk8054/openphish-adblock/blob/main/domain_paths.txt), that domain-path will be used in the filter list,
- If a URL matches one of the domain web hosts in [`domain_web_hosts.txt`](https://github.com/stephenhawk8054/openphish-adblock/blob/main/domain_web_hosts.txt), only domain in the URL will be used and its path will be ignored,
- If a URL matches some conditions in [`custom.py`](https://github.com/stephenhawk8054/openphish-adblock/blob/main/custom.py), only domain in the URL will be used and its path will be ignored,
- Dead domains are removed at least once a week using [Adguard's Dead Domains Linter](https://github.com/AdguardTeam/DeadDomainsLinter)

## How to use

- Install [`orjson`](https://github.com/ijl/orjson) for Python 3.12+

```
pip install orjson
```

- Install [Adguard's Dead Domains Linter](https://github.com/AdguardTeam/DeadDomainsLinter#installation-and-update)

- To fetch the feed and update the filters, run

```
python main.py
```

- To check dead domains and update the filters, run

```
python check_dd.py
python main.py
```

## About

[GPLv3 License](https://github.com/stephenhawk8054/openphish-adblock/blob/main/LICENSE)
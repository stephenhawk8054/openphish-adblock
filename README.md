# openphish-adblock
Openphish feed in adblock syntaxes

The filter list is curated from [OpenPhish](https://openphish.com/). The URL feed is fetched from [OpenPhish Free Phishing Feed](https://openphish.com/feed.txt) at least twice per day. Compatible with uBlock Origin, Adguard, Adblock Plus...

---

## Links for adding to blocker extensions

- jsDelivr: https://cdn.jsdelivr.net/gh/stephenhawk8054/openphish-adblock@latest/filters.txt
- Statically: https://cdn.statically.io/gh/stephenhawk8054/openphish-adblock/main/filters.txt?dev=1

---

## Some modifications comparing to original feeds

- Ignore queries (`?`, `&`) and fragments (`#`) in the URLs,
- Ignore `www.` at the start of the domains,
- If a URL matches one of URL/domain paths in [`domain_paths.txt`](https://github.com/stephenhawk8054/openphish-adblock/blob/main/domain_paths.txt), that domain-path will be used in the filter list,
- If a URL matches one of the domain web hosts in [`domain_web_hosts.txt`](https://github.com/stephenhawk8054/openphish-adblock/blob/main/domain_web_hosts.txt), only domain will be used and its path will be ignored.
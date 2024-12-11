import platform
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from time import sleep
from urllib.parse import urlsplit

from custom import use_domain
from utils import clean_split, load_json, load_text, write_json, write_text

HOSTS = list(load_text('domain_web_hosts.txt', True))
PATHS = list(load_text('domain_paths.txt', True))

def craft_domain(url: str) -> str:
    split_url = urlsplit(url)

    # Currently ignoring queries and fragments
    # Check custom conditions
    if use_domain(domain := split_url.netloc.removeprefix('www.'), url):
        return domain

    for web_host in HOSTS:
        if domain.endswith(web_host):
            return domain

    # Prioritize PATHS first
    for domain_path in PATHS:
        if '/' in domain_path:
            continue

        if domain.endswith(domain_path):
            return domain_path
        
    if split_url.path.rstrip('.~!/'):
        return None
    
    return domain

def craft_url(url: str) -> str:
    split_url = urlsplit(url)

    # Currently ignoring queries and fragments
    url_query = ''
    url_block = (domain := split_url.netloc).removeprefix('www.')

    # Prioritize PATHS first
    for domain_path in PATHS:
        if not domain.endswith(domain_path.split('/')[0]):
            continue
        
        if url.lower().rstrip('.~!/').endswith(domain_path.lower().rstrip('.~!/')):
            return domain, domain_path.rstrip('.~!/')

        if domain_path.lower() in url.lower():
            return domain, domain_path.rstrip('.~!/')

    for web_host in HOSTS:
        if url_block.endswith(web_host):
            return domain, url_block
        
    # Check custom conditions
    if use_domain(domain, url):
        return domain, domain

    # Ends at .html and .php
    if '.html' in (url_path := f'{split_url.path}{url_query}'):
        url_path = url_path.split('.html')[0] + '.html'

    if '.php' in url_path:
        url_path = url_path.split('.php')[0] + '.php'

    # Clean dirty URL
    url_block += next(clean_split(url_path, '[*$]')).rstrip('.~!')
    
    return domain, url_block.rstrip('.~!/')

def main():
    # Sometimes we don't want to fetch the feed again
    fetch = input('\nFetch feed? (y/n)\n>>> ').lower()
    if fetch not in ('y', 'yes', 'n', 'no'):
        exit()

    while True:
        feeds: dict[str, str] = load_json('feeds.json')

        # TODO: Implement a better ignore / whitelist process
        # =================================================================================
        # 
        for url in load_text('ignore.txt', True):
            feeds.pop(url, None)
        # 
        # ignore_urls = set(load_text('ignore.txt', True))
        # whitelist = set()
        # whitelist_txt = list(load_text('whitelist.txt', True))
        # for url in feeds.keys():
        #     if url in ignore_urls:
        #         whitelist.add(url)
        #         continue
        #     for whitelist_url in whitelist_txt:
        #         if whitelist_url.startswith('!'): continue
        #         if whitelist_url not in url: continue
        #         whitelist.add(url)    
        # for url in whitelist:
        #     feeds.pop(url, None)
        # 
        # =================================================================================

        # We'll put current UTC date time to "Last modified" section
        dt = datetime.now(timezone.utc).isoformat(timespec='milliseconds')

        if fetch in ('y', 'yes'):
            req = urllib.request.Request('https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt', method='GET')

            while True:
                try:
                    with urllib.request.urlopen(req) as response:
                        data: bytes = response.read()
                        if response.status == 200:
                            write_text(data.decode().strip(), 'feed.txt')
                            break
                except urllib.error.URLError as e:
                    print(e)
                    
                sleep(300)

            ddl_cmd = 'dead-domains-linter'
            if platform.system() == 'Windows':
                ddl_cmd += '.cmd'

            subprocess.run([ddl_cmd, '-i', 'feed.txt', '--export', 'dead_domains.txt'])

            # Remove dead domains from new URLs
            dead_domains = set(load_text('dead_domains.txt', True))
            for url in load_text('feed.txt', True):
                if craft_url(url)[0] in dead_domains:
                    feeds.pop(url, None)
                    continue
                
                # Overwrite the current date, so we can remove old URLs later
                feeds[url] = dt
        
        # Old way
        # =================================================================================
        # 
        # Don't duplicate filters
        # filters_set = set()
        # def yield_filter():
        #     for url in feeds.keys():
        #         if (url_block := craft_url(url)[1]).lower() in filters_set: continue

        #         filters_set.add(url_block.lower())
                
        #         if not url_block.startswith(":"):
        #             url_block = f'||{url_block}'
        #         yield f'{url_block}^$document,subdocument,popup'
        
        # write_json(feeds, 'feeds.json')
        # write_text(yield_filter(), 'filters_init.txt')
        # 
        # =================================================================================

        # New way
        # Use set to check faster
        filters_set, domains_set = set(), set()

        # Store final filters
        filters_url, filters_domain = [], []

        # Start to run on feeds.json
        for url in feeds.keys():
            if (url_block := craft_url(url)[1]).lower() in filters_set: continue
            
            filters_set.add(url_block.lower())

            # Craft filters for full URL
            if not url_block.startswith(":"):
                url_block = f'||{url_block}^'

            filters_url.append(f'{url_block}$document,subdocument,popup')

            # Craft filters for domain
            if (domain := craft_domain(url.lower())) and domain not in domains_set:
                domains_set.add(domain)
                filters_domain.append(f'||{domain}^')

        write_json(feeds, 'feeds.json')
        write_text(filters_url, 'filters_init.txt')
        write_text(filters_domain, 'filters_init_domains.txt')

        # Modify "Last modified" date
        # URL list
        text_list = []
        for line in load_text('filters.txt', True):
            if 'Last modified' in line:
                text_list.append(f'! Last modified: {dt}')
            elif 'filters_init.txt' in line:
                text_list.append(f'\n{line}')
            else:
                text_list.append(line)
        write_text(text_list, 'filters.txt')

        # Domain list
        domain_list = []
        for line in load_text('filters_domains.txt', True):
            if 'Last modified' in line:
                domain_list.append(f'! Last modified: {dt}')
            elif 'filters_init_domains.txt' in line:
                domain_list.append(f'\n{line}')
            else:
                domain_list.append(line)
        write_text(domain_list, 'filters_domains.txt')

        if fetch in ('n', 'no'):
            exit()

        sleep(3600)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
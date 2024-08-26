import platform
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from time import sleep
from urllib.parse import urlsplit

from utils import clean_split, load_json, load_text, write_json, write_text

HOSTS = list(load_text('domain_web_hosts.txt', True))
PATHS = list(load_text('domain_paths.txt', True))

def craft_url(url: str) -> str:
    split_url = urlsplit(url)

    # Currently ignoring queries and fragments
    # url_query = f'?{split_url.query}' if split_url.query else ''
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

    if '.html' in (url_path := f'{split_url.path}{url_query}'):
        url_path = url_path.split('.html')[0] + '.html'

    if '.php' in url_path:
        url_path = url_path.split('.php')[0] + '.php'

    url_block += next(clean_split(url_path, '[*$]')).rstrip('.~!')
    
    return domain, url_block.rstrip('.~!/')

def main():
    # Sometimes we don't want to fetch the feed again
    fetch = input('\nFetch feed? (y/n)\n>>> ').lower()
    if fetch not in ('y', 'yes', 'n', 'no'):
        exit()

    while True:
        feeds = load_json('feeds.json')

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
            req = urllib.request.Request('https://openphish.com/feed.txt', method='GET')

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

            # Remove dead domains from feeds.json
            dead_domains = set(load_text('dead_domains.txt', True))
            for url in load_text('feed.txt', True):
                if craft_url(url)[0] in dead_domains:
                    feeds.pop(url, None)
                    continue
                
                # Overwrite the current date, so we can remove old URLs later
                feeds[url] = dt
        
        # Don't duplicate filters
        filters_set = set()
        def yield_filter():
            for url in feeds.keys():
                if (url_block := craft_url(url)[1]).lower() in filters_set: continue

                filters_set.add(url_block.lower())
                
                if not url_block.startswith(":"):
                    url_block = f'||{url_block}'
                yield f'{url_block}^$document,subdocument,popup'
        
        write_json(feeds, 'feeds.json')
        write_text(yield_filter(), 'filters_init.txt')

        # Modify "Last modified" date
        text_list = []
        for line in load_text('filters.txt', True):
            if 'Last modified' in line:
                text_list.append(f'! Last modified: {dt}')
            elif 'filters_init.txt' in line:
                text_list.append(f'\n{line}')
            else:
                text_list.append(line)
        write_text(text_list, 'filters.txt')

        if fetch in ('n', 'no'):
            exit()

        sleep(3600)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
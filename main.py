import platform
import subprocess
import urllib.request
from datetime import datetime, timezone
from time import sleep
from urllib.parse import urlsplit

from utils import clean_split, load_json, load_text, write_json, write_text


def craft_url(url: str) -> str:
    split_url = urlsplit(url)

    # url_query = f'?{split_url.query}' if split_url.query else ''
    url_query = ''
    url_block = (domain := split_url.netloc.split(':')[0]).removeprefix('www.')

    for web_host in load_text('domain_web_hosts.txt', True):
        if url_block.endswith(web_host):
            return domain, url_block

    if '.html' in (url_path := f'{split_url.path}{url_query}'):
        url_path = url_path.split('.html')[0] + '.html'

    if '.php' in url_path:
        url_path = url_path.split('.php')[0] + '.php'

    url_block += next(clean_split(url_path, '[*$]')).rstrip('.~!')
    
    return domain, url_block.rstrip('.~!/')

def main():
    req = urllib.request.Request('https://openphish.com/feed.txt', method='GET')

    while True:
        with urllib.request.urlopen(req) as response:
            data: bytes = response.read()
            if response.status == 200:
                write_text(data.decode().strip(), 'feed.txt')
                break
        sleep(300)

    ddl_cmd = 'dead-domains-linter'
    if platform.system() == 'Windows':
        ddl_cmd += '.cmd'

    subprocess.run([ddl_cmd, '-i', 'feed.txt', '--export', 'dead_domains.txt'])

    feeds = load_json('feeds.json')
    
    for url in load_text('ignore.txt', True):
        feeds.pop(url, None)

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

    dt = datetime.now(timezone.utc).isoformat(timespec='milliseconds')

    dead_domains = set(load_text('dead_domains.txt', True))
    for url in load_text('feed.txt', True):
        if craft_url(url)[0] in dead_domains:
            feeds.pop(url, None)
            continue
        
        feeds[url] = dt
    
    filters_set = set()
    def yield_filter():
        for url in feeds.keys():
            if (url_block := craft_url(url)[1]) in filters_set: continue

            filters_set.add(url_block)
            yield f'||{url_block}^$document,subdocument,popup'
    
    write_json(feeds, 'feeds.json')
    write_text(yield_filter(), 'filters_init.txt')

    text_list = []
    for line in load_text('filters.txt', True):
        if 'Last modified' in line:
            text_list.append(f'! Last modified: {dt}')
        elif 'filters_init.txt' in line:
            text_list.append(f'\n{line}')
        else:
            text_list.append(line)
    write_text(text_list, 'filters.txt')

if __name__ == "__main__":
    while True:
        main()
        sleep(3600)
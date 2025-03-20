import platform
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

from utils import load_json, load_text, write_json, write_text

# Set command based on OS
ddl_cmd = 'dead-domains-linter'
if platform.system() == 'Windows':
    ddl_cmd += '.cmd'

def ddl_cli(urls: list[str]):
    # Prepare all URLs first
    write_text(urls, 'ddl/feeds.txt')

    # Double check dead domains as it can depend on the network
    try:
        subprocess.run([ddl_cmd, '-i', 'ddl/feeds.txt', '--export', 'ddl/dead_domains.txt'])
    except KeyboardInterrupt:
        exit()

# domain_paths info
domain_paths = set(line for line in load_text('domain_paths.txt', True) if '/' not in line)

# Gather all feeds
feeds: dict[str, dict[str, str]] = {'feeds.json': load_json('feeds.json')}

# Get archive feeds to process separately
archive_domains = set()
archive_list = []
for file_path in Path('archive').iterdir():
    feeds[f'archive/{file_path.name}'] = (feed := load_json(file_path))

    print(f'Extracting URLs in {file_path.name} ...')
    for url in feed.keys():
        # We don't want to process same domains
        if (domain := urlsplit(url).netloc.split(':')[0].removeprefix('www.')) in archive_domains:
            continue
        
        archive_domains.add(domain)

        # Search subdomain to domain_paths
        domain_split = domain.split('.')
        for idx in reversed(range(len(domain_split) - 1)):
            subdomain = '.'.join(domain_split[idx:])
            if subdomain in domain_paths:
                archive_list.append(url)
                break

# Check dead domain of archive URLs first
ddl_cli(archive_list)
archive_dead = set(load_text('ddl/dead_domains.txt', True))

for file_name, feed in feeds.items():
    print(f'Check dead domains in {file_name} ...')

    # Get all URLs
    urls = [url for url in feed.keys()]

    # Check dead domain on only feeds.json, otherwise just remove item
    if file_name == 'feeds.json':
        ddl_cli(urls)
        dead_domains = set(load_text('ddl/dead_domains.txt', True))
    else:
        dead_domains = archive_dead

    for url in urls:
        if urlsplit(url).netloc.split(':')[0] not in dead_domains:
            continue
        feeds[file_name].pop(url, None)

input('\nPlease check dead domains again...')

for file_name, feed in feeds.items():
    write_json(feed, file_name)
import platform
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

from utils import load_json, load_text, write_json, write_text

# Set command based on OS
ddl_cmd = 'dead-domains-linter'
if platform.system() == 'Windows':
    ddl_cmd += '.cmd'

# Gather all feeds
feeds: dict[str, dict[str, str]] = {'feeds.json': load_json('feeds.json')}
for file_path in Path('archive').iterdir():
    feeds[f'archive/{file_path.name}'] = load_json(file_path)

for file_name in feeds.keys():
    print(f'Check dead domains in {file_name} ...')

    # Prepare all URLs first
    write_text((urls := [url for url in feeds[file_name].keys()]), 'feeds.txt')

    # Double check dead domains as it can depend on the network
    try:
        subprocess.run([ddl_cmd, '-i', 'feeds.txt', '--export', 'dead_domains.txt'])
    except KeyboardInterrupt:
        exit()

    dead_domains = set(load_text('dead_domains.txt', True))

    for url in urls:
        if urlsplit(url).netloc.split(':')[0] not in dead_domains: continue
        feeds[file_name].pop(url, None)

input('\nPlease check dead domains again...')

for file_name, feed in feeds.items():
    write_json(file_name, feed)
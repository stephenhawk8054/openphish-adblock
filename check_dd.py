import platform
import subprocess
from urllib.parse import urlsplit

from utils import load_json, load_text, write_json, write_text

feeds: dict[str, str] = load_json('feeds.json')
# Prepare all URLs first
write_text((urls := [url for url in feeds.keys()]), 'feeds.txt')

ddl_cmd = 'dead-domains-linter'
if platform.system() == 'Windows':
    ddl_cmd += '.cmd'

# Double check dead domains as it can depend on the network
try:
    subprocess.run([ddl_cmd, '-i', 'feeds.txt', '--export', 'dead_domains.txt'])
    input('\nPlease check dead domains again...')
except KeyboardInterrupt:
    exit()

dead_domains = set(load_text('dead_domains.txt', True))

for url in urls:
    if urlsplit(url).netloc.split(':')[0] not in dead_domains: continue
    feeds.pop(url, None)

write_json(feeds, 'feeds.json')
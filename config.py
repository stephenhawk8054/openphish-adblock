from utils import load_text

# main
HOSTS = list(load_text('domain_web_hosts.txt', True))
PATHS = list(load_text('domain_paths.txt', True))
START = 2024
DAYS = 90

# custom
PATH_ENDS = list(load_text('compare/path_ends.txt', True))
PATH_CONTAINS = list(load_text('compare/path_contains.txt', True))
PATH_EQUALS = list(load_text('compare/path_equals.txt', True))
PATH_STARTS = list(load_text('compare/path_starts.txt', True))
DOMAIN_ENDS = list(load_text('compare/domain_ends.txt', True))
DOMAIN_STARTS = list(load_text('compare/domain_starts.txt', True))
LEGIT_DOMAINS = list(load_text('compare/legit_domains.txt', True))
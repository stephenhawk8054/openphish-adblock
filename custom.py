import re

from utils import compare, load_text

PATH_CONTAINS = list(load_text('compare/path_contains.txt', True))
PATH_EQUALS = list(load_text('compare/path_equals.txt', True))
PATH_STARTS = list(load_text('compare/path_starts.txt', True))
DOMAIN_ENDS = list(load_text('compare/domain_ends.txt', True))
DOMAIN_STARTS = list(load_text('compare/domain_starts.txt', True))

def use_domain(domain: str, path: str, verbose: bool = False) -> bool:
    # Use domain if path is too short
    if (
        len(path.rstrip('.~!/')) <= 3 and
        domain not in (
            'gx.ax',
            'reactstudio.it',
            'supermario-game.com'
        )
    ):
        if verbose:
            print_domain(domain, path)
        return True

    # .com- cases
    if '.com-' in domain:
        return True

    # Social media
    if (
        domain.startswith('server.') and
        domain.endswith('.com') and
        path.startswith('/invite/')
    ):
        return True

    # USPS
    if (
        domain.startswith('info-tracking') and
        domain.endswith('.cc')
    ):
        return True

    # Telegram
    if (
        domain.startswith('telegram-') and
        domain.endswith('.com') and
        path.startswith('/login/index.html')
    ):
        return True

    # Bet365
    if (
        domain.startswith('bte') and
        domain.endswith('.com') and
        path.startswith('/home')
    ):
        return True

    # Auto return with matched strings
    if (
        compare(domain, DOMAIN_ENDS, 'endswith') or
        compare(domain, DOMAIN_STARTS, 'startswith') or
        compare(path.rstrip('.~!/'), PATH_EQUALS, 'equals') or
        compare(path, PATH_STARTS, 'startswith') or
        compare(path, PATH_CONTAINS, 'contains')
    ):
        return True

    # =========================================================================
    # REMIND: always put these at end because of regex
    
    # Bet365
    if (
        domain.endswith('.com') and
        re.match(r'^bet\d', domain)
    ):
        return True

    # .cc
    if re.match(r'^\d+\.(?:cc|com)$', domain):
        return True
    
    # Steam
    if (
        domain.startswith('steam.') and
        len(domain.split('.')) >= 3
    ):
        return True

    if (
        domain == 'steamcommunity.com' or
        not domain.endswith('.com')
    ):
        return False

    if (
        not domain.startswith('st') and
        not domain.startswith('sc')
    ):
        return False

    if re.match(r'^s[ct][ace][ae][a-z]{1,4}o[mn][a-z]{4,8}y[a-z]?\.com$', domain):
        return True
    
    return False

def print_domain(domain: str, path: str):
    if (
        not domain.endswith('.top') and
        not domain.endswith('.icu') and
        not domain.endswith('.github.io') and
        not domain.startswith('usps.com-') and
        len(path) == 3
    ):
        print(domain + path)
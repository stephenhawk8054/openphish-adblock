import re

from utils import compare, load_text

DOMAIN_ENDS = list(load_text('domain_ends.txt', True))
DOMAIN_STARTS = list(load_text('domain_starts.txt', True))

def use_domain(domain: str, path: str, verbose: bool = False) -> bool:
    # Use domain if path is too short
    if (
        len(path) <= 3 and
        domain not in (
            'gx.ax',
            'reactstudio.it',
            'supermario-game.com'
        )
    ):
        if verbose:
            print_domain(domain, path)
        return True
    
    # Auto return domain with endings or startings
    if (
        compare(domain, DOMAIN_ENDS, 'endswith') or
        compare(domain, DOMAIN_STARTS, 'startswith')
    ):
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
    
    # Steam
    if (
        domain.startswith('steam.') and
        len(domain.split('.')) >= 3
    ):
        return True

    if (
        domain == 'steamcommunity.com' or
        not domain.startswith('st') or
        not domain.endswith('.com')
    ):
        return False
    
    steam_patterns = [
        r'^st[ace][ae][a-z]{1,4}o[mn][a-z]{4,8}y[a-z]?\.com$',
        # r'^stae[a-z]{1,4}o[mn][a-z]{4,7}y[a-z]?\.com$',
    ]
    for steam_pattern in steam_patterns:
        if re.match(steam_pattern, domain):
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
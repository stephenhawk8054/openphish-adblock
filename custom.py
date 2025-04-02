import re

from config import (
    DOMAIN_ENDS,
    DOMAIN_STARTS,
    LEGIT_DOMAINS,
    # PATH_CONTAINS,
    # PATH_ENDS,
    PATH_EQUALS,
    PATH_STARTS,
)
from utils import compare


def use_domain(domain: str, url_path: str, verbose: bool = False) -> bool:
    # Ignore legit domains
    if (
        compare(f'://{domain}/', LEGIT_DOMAINS, 'endswith') or
        compare(f'://{domain}/', LEGIT_DOMAINS, 'startswith')
    ):
        return False

    # Use domain if url_path is too short
    if (
        len(url_path.rstrip('.~!/')) <= 3 and
        domain not in (
            'gx.ax',
            'reactstudio.it',
            'supermario-game.com'
        )
    ):
        if verbose:
            print_domain(domain, url_path)
        return True

    # .com- cases
    if '.com-' in domain:
        return True

    # Social media
    if (
        domain.startswith('server.') and
        domain.endswith('.com') and
        url_path.startswith('/invite/')
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
        url_path.startswith('/login/index.html')
    ):
        return True

    # Bet365
    if (
        domain.startswith('bte') and
        domain.endswith('.com') and
        url_path.startswith('/home')
    ):
        return True

    # Webmail
    if (
        url_path.startswith('/accounts/19') and
        ('/messages/' in url_path) and
        ('/clicks/' in url_path)
    ):
        return True

    # Auto return with matched strings
    # https://github.com/uBlockOrigin/uAssets/issues/27817
    if (
        compare(domain, DOMAIN_ENDS, 'endswith') or
        compare(domain, DOMAIN_STARTS, 'startswith') or
        compare(url_path.rstrip('.~!/').lower(), PATH_EQUALS, 'equals') or
        compare(url_path, PATH_STARTS, 'startswith')
    ):
        return True

    # =========================================================================
    # REMIND: always put these at end because of regex

    # Telegram
    if (
        domain.startswith('telegram') and
        domain.endswith('.com') and
        re.match(r'telegram[a-z]{2}\.com$', domain)
    ):
        return True

    # Facebook
    if (
        url_path.startswith('/help/contact/') and
        re.match(r'^\/help\/contact\/\d{15,17}\b', url_path)
    ):
        return True
    
    # Bet365
    if (
        domain.endswith('.com') and
        re.match(r'^bet\d', domain)
    ):
        return True

    # /order/
    if (
        url_path.startswith('/order/') and
        re.match(r'^\/order\/[a-zA-Z0-9]{12}$', url_path.rstrip('.~!/'))
    ):
        return True

    # Number
    if re.match(r'^\d+\.(?:cc|com|xyz)$', domain):
        return True
    
    # Steam
    if domain.startswith('steamcommunity.'):
        return True

    if (
        domain.startswith('steam.') and
        len(domain.split('.')) >= 3
    ):
        return True

    if 'steampowered.' in domain:
        return True

    if (
        not domain.startswith('st') and
        not domain.startswith('sc') and
        not domain.startswith('sz')
    ):
        return False

    if (
        not domain.endswith('.com') and
        not domain.endswith('.ru')
    ):
        return False

    if re.match(r'^s[cftz]y?[ace][aemnu][a-z]{1,4}o[mn][a-z]{4,8}[iy][a-z]?\.(?:com|ru)$', domain):
        return True
    
    return False

def print_domain(domain: str, url_path: str):
    if (
        not domain.endswith('.top') and
        not domain.endswith('.icu') and
        not domain.endswith('.github.io') and
        not domain.startswith('usps.com-') and
        len(url_path) == 3
    ):
        print(domain + url_path)
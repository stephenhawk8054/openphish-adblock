import re
from urllib.parse import SplitResult


def use_domain(domain: str, split_url: SplitResult, verbose: bool = False) -> bool:
    # Use domain if path is too short
    if (
        len(split_url.path) <= 3 and
        domain not in ['gx.ax']
    ):
        if verbose:
            if len(split_url.path) == 3:
                print(domain + split_url.path)
        return True
    
    # Auto return with .top TLD
    if (
        domain.endswith('.top') or
        domain.startswith('usps.com-')
    ):
        return True

    # Telegram
    if (
        domain.startswith('telegram-') and
        domain.endswith('.com') and
        split_url.path.startswith('/login/index.html')
    ):
        return True
    
    # Steam regex
    if (
        domain == 'steamcommunity.com' or
        not domain.startswith('st') or
        not domain.endswith('.com')
    ):
        return False
    
    steam_patterns = [
        r'^ste[ae][a-z]{1,4}o[mn][a-z]{4,7}y[a-z]?\.com$',
        r'^stae[a-z]{1,4}o[mn][a-z]{4,7}y[a-z]?\.com$',
    ]
    for steam_pattern in steam_patterns:
        if re.match(steam_pattern, domain):
            return True
    
    return False
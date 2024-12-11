import re
from urllib.parse import urlsplit


def use_domain(domain: str, url: str) -> bool:
    if (
        domain.endswith('.top') or
        domain.startswith('usps.com-')
    ): 
        return True
    
    # Steam regex
    if domain == 'steamcommunity.com': return False
    steam_patterns = [
        r'^ste[ae][a-z]{1,4}o[mn][a-z]{4,7}y[a-z]?\.com$',
        r'^stae[a-z]{1,4}o[mn][a-z]{4,7}y[a-z]?\.com$',
    ]
    for steam_pattern in steam_patterns:
        if re.match(steam_pattern, domain): return True

    # Telegram
    if domain.startswith('telegram-') and '.com/login/index.html' in url:
        return True
    
    return False
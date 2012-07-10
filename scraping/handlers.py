
registry = {}

def register(scraper, callable_):
    registry[scraper] = callable_
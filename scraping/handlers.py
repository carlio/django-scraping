
registry = {}

def register(scraper, callable):
    registry[scraper] = callable
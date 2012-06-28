
registry = {}

def register(callable, page_type):
    registry[page_type] = callable
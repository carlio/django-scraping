from scraping.handlers import register

def handler(name):
    def decorator(func):
        register(name, func)
        return func
    return decorator


from django.utils import importlib
import imp
from django.conf import settings


def autodiscover():
    """
    Automatically build the site index.

    Again, almost exactly as django.contrib.admin does things, for consistency.
    """

    for app in settings.INSTALLED_APPS:
        # For each app, we need to look for an search_indexes.py inside that app's
        # package. We can't use os.path here -- recall that modules may be
        # imported different ways (think zip files) -- so we need to get
        # the app's __path__ and look for handlers.py on that path.

        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own index registration.
        try:
            app_path = importlib.import_module(app).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's handlers.py. For some
        # reason imp.find_module raises ImportError if the app can't be found
        # but doesn't actually try to import the module. So skip this app if
        # its handlers.py doesn't exist
        try:
            imp.find_module('handlers', app_path)
        except ImportError:
            continue

        # Step 3: import the app's handlers file. If this has errors we want them
        # to bubble up.
        importlib.import_module("%s.handlers" % app)

autodiscover()

# Yuck... I don't like this but not sure what else to do. Since
# celery tasks are registered via their metaclass, tasks can
# only be registered if they are imported from somewhere. That
# is not guaranteed to happen in django applications using this
# library, so without requiring an additional setting in settings.py
# this is probably the best I can do to force tasks to be imported
# and therefore registered.
from tasks import *
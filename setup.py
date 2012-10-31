# -*- coding: UTF-8 -*-
from distutils.core import setup
from setuptools import find_packages
import time


_version = "0.%s.dev" % int(time.time())
_packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
    
# common dependencies
_install_requires = [
            'django',
            'django-annoying',
            'celery',
            'pyquery',
            'requests',
            
            'feedparser',
            'Pillow', # TODO: make this an optional dependency
            
            'django-gubbins<1',
       ]

setup( name='django-scraping',
       url='https://github.com/carlio/django-scraping',
       author='Carl Crowder',
       author_email='django-scraping@jqx.be',
       version=_version,
       packages=_packages,
       install_requires=_install_requires,
       scripts=[
           # 'scripts/manage',
       ],
)

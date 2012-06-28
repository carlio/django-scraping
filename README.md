django-scraping
===============



Other Dependencies
==================

django-scraping relies upon PyQuery which in turn relies upon lxml. In order to
install lxml, you must have a compiler and development versions of python,
libxml2 and libxslt available.

See also http://lxml.de/build.html


Optional Dependencies
=====================

Some features require additional dependencies to be manually installed, because
the features are rarely used or because the dependency is "difficult" to install
(such as a dependency requiring native compilation against packages 

* For dealing with images, Pillow is required
  - see also http://pypi.python.org/pypi/Pillow#build-instructions-all-platforms

from pyquery import PyQuery as pq
import re

def pyquery_from_xml(xml):
    # remove the namespace so we can use PyQuery (as
    # PyQuery fails when trying to use namespaces in selectors due to
    # an underlying lxml bug - see https://bitbucket.org/olauzanne/pyquery/issue/17/pyquery-fails-when-trying-to-query-a
    xml = re.sub('xmlns.*?".*?"', '', xml)
    return pq(xml)
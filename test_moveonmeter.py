from xml.etree import ElementTree

from moveonmeter import htmlump


def test_htmlump_valid_xml():
    ElementTree.fromstring(htmlump)

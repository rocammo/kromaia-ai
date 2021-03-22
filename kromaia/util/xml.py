import xml.etree.ElementTree as ET


def values(elements, node, tag):
    return [element[node].get(tag) for element in elements]

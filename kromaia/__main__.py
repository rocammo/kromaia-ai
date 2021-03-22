from .util import xml
from .util.log import Log

verbose = True


def parse_xml(file):
    import xml.etree.ElementTree as ET
    vermis = ET.parse(file).getroot()

    hulls = vermis.findall("HULL/Hull")
    links = vermis.findall("HULL/LINKS/Link")

    log.vprint("No. of Hull: %s\n" % len(hulls))
    log.vprint("No. of Link: %s\n" % len(links))


def main():
    parse_xml("objects/Vermis.xml")


if __name__ == '__main__':
    global log
    log = Log(verbose=verbose)

    main()

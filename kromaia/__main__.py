import argparse

from .util import xml
from .util import config
from .util.log import Log
from .math.vector3 import Vector3


def init():
    parser = argparse.ArgumentParser(description="Exploring program synthesis in model-driven engineering "
                                     "through machine learning techniques in Kromaia scenario.")
    parser.add_argument("environment", metavar="environment", type=str,
                        help="run with environment (values: 'dev' or 'prod')")

    args = parser.parse_args()
    environment = config.get_config("kromaia.env.json", args.environment)

    global log
    log = Log(verbose=environment["verbose"])


def parse_xml(file):
    import xml.etree.ElementTree as ET
    vermis = ET.parse(file).getroot()

    hulls = vermis.findall("HULL/Hull")
    links = vermis.findall("HULL/LINKS/Link")

    log.vprint("No. of Hull: %s\n" % len(hulls))
    log.vprint("No. of Link: %s\n" % len(links))

    scalesX = xml.values(hulls, 0, "ScaleX")
    scalesY = xml.values(hulls, 0, "ScaleY")
    scalesZ = xml.values(hulls, 0, "ScaleZ")
    scales = [Vector3(scalesX[i], scalesY[i], scalesZ[i])
              for i in range(len(hulls))]

    log.vprint(f"Scales: {scales}\n")


def run():
    parse_xml("objects/Vermis.xml")


if __name__ == '__main__':
    init()
    run()

import argparse

from .util import xml
from .util import config
from .util.log import Log

from .math.vector3 import Vector3
from .math.quaternion import Quaternion

from .entities.hull import Hull
from .entities.link import Link


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

    log.vprint("No. of Hull: %s\nNo. of Link: %s\n" % (len(hulls), len(links)))

    return hulls, links


def get_hulls_components(hulls):
    scalesX = xml.values(hulls, 0, "ScaleX")
    scalesY = xml.values(hulls, 0, "ScaleY")
    scalesZ = xml.values(hulls, 0, "ScaleZ")
    scales = [Vector3(scalesX[i], scalesY[i], scalesZ[i])
              for i in range(len(hulls))]

    log.vprint(f"Scales: {scales}\n")

    positionsX = xml.values(hulls, 0, "PositionX")
    positionsY = xml.values(hulls, 0, "PositionY")
    positionsZ = xml.values(hulls, 0, "PositionZ")
    positions = [Vector3(positionsX[i], positionsY[i], positionsZ[i])
                 for i in range(len(hulls))]

    log.vprint(f"Positions: {positions}\n")

    orientationsW = xml.values(hulls, 0, "OrientationW")
    orientationsX = xml.values(hulls, 0, "OrientationX")
    orientationsY = xml.values(hulls, 0, "OrientationY")
    orientationsZ = xml.values(hulls, 0, "OrientationZ")
    orientations = [Quaternion(orientationsW[i], orientationsX[i],
                               orientationsY[i], orientationsZ[i]) for i in range(len(hulls))]

    log.vprint(f"Orientations: {orientations}\n")

    return scales, positions, orientations


def get_links_components(links):
    hull_index_first = xml.values(links, 0, "HullIndexFirst")
    hull_index_second = xml.values(links, 0, "HullIndexSecond")

    return hull_index_first, hull_index_second


def run():
    hulls, links = parse_xml("objects/Vermis.xml")

    # Hulls.
    scales, positions, orientations = get_hulls_components(hulls)
    hulls_ = [Hull(scales[i], positions[i], orientations[i])
              for i in range(len(hulls))]
    for i in range(len(hulls)):
        log.vprint(f"{hulls_[i]}")
    log.vprint("")  # newline

    # Links.
    hull_index_first, hull_index_second = get_links_components(links)
    links_ = [Link(hull_index_first[i], hull_index_second[i])
              for i in range(len(links))]
    for i in range(len(links)):
        log.vprint(f"{links_[i]}")
    log.vprint("")  # newline

    # Hulls indexed by links.
    hulls_indexed = set()
    for i in range(len(links)):
        hulls_indexed.add(int(links_[i].hull_index_first))
        hulls_indexed.add(int(links_[i].hull_index_second))
    log.vprint(f"HullIndexParent (TOT-{len(hulls_indexed)}): {hulls_indexed}")


if __name__ == '__main__':
    init()
    run()

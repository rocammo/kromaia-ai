from kromaia.util import xml
from kromaia.util.config import log

from kromaia.math.vector3 import Vector3
from kromaia.math.quaternion import Quaternion


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

from kromaia.util import xml
from kromaia.util.config import log
from kromaia.util.colors import bcolors

from kromaia.math.vector3 import Vector3
from kromaia.math.quaternion import Quaternion

from kromaia.entities.hull import Hull
from kromaia.entities.link import Link


def parse_xml(file):
    import xml.etree.ElementTree as ET
    vermis = ET.parse(file).getroot()

    hulls = vermis.findall("HULL/Hull")
    links = vermis.findall("HULL/LINKS/Link")

    log.vprint(f"{bcolors.OKBLUE}No. of Hull: %s\nNo. of Link: %s{bcolors.ENDC}\n" % (
        len(hulls), len(links)))

    return hulls, links


def get_hulls_components(hulls):
    scalesX = xml.values(hulls, 0, "ScaleX")
    scalesY = xml.values(hulls, 0, "ScaleY")
    scalesZ = xml.values(hulls, 0, "ScaleZ")
    scales = [Vector3(scalesX[i], scalesY[i], scalesZ[i])
              for i in range(len(hulls))]

    # log.vprint(f"Scales: {scales}\n")

    positionsX = xml.values(hulls, 0, "PositionX")
    positionsY = xml.values(hulls, 0, "PositionY")
    positionsZ = xml.values(hulls, 0, "PositionZ")
    positions = [Vector3(positionsX[i], positionsY[i], positionsZ[i])
                 for i in range(len(hulls))]

    # log.vprint(f"Positions: {positions}\n")

    orientationsW = xml.values(hulls, 0, "OrientationW")
    orientationsX = xml.values(hulls, 0, "OrientationX")
    orientationsY = xml.values(hulls, 0, "OrientationY")
    orientationsZ = xml.values(hulls, 0, "OrientationZ")
    orientations = [Quaternion(orientationsW[i], orientationsX[i],
                               orientationsY[i], orientationsZ[i]) for i in range(len(hulls))]

    # log.vprint(f"Orientations: {orientations}\n")

    return scales, positions, orientations


def get_links_components(links):
    hull_index_first = xml.values(links, 0, "HullIndexFirst")
    hull_index_second = xml.values(links, 0, "HullIndexSecond")

    return hull_index_first, hull_index_second


def get_hulls(hulls):
    scales, positions, orientations = get_hulls_components(hulls)
    hulls_ = [Hull(scales[i], positions[i], orientations[i])
              for i in range(len(hulls))]
    for i in range(len(hulls)):
        log.vprint(f"{hulls_[i]}")
    log.vprint("")  # newline

    return hulls_


def get_links(links):
    hull_index_first, hull_index_second = get_links_components(links)
    links_ = [Link(hull_index_first[i], hull_index_second[i])
              for i in range(len(links))]
    for i in range(len(links)):
        log.vprint(f"{links_[i]}")
    log.vprint("")  # newline

    return links_


def get_hulls_indexed_by_links(links):
    hulls_indexed = set()
    for i in range(len(links)):
        hulls_indexed.add(int(links[i].hull_index_first))
        hulls_indexed.add(int(links[i].hull_index_second))
    log.vprint(
        f"{bcolors.OKCYAN}HullIndexParent{bcolors.ENDC} (TOT-{len(hulls_indexed)}): {hulls_indexed}\n")

    return hulls_indexed


def to_dataset(name, hulls, links):
    dataset = []

    for j in range(len(links)):
        hull_index_first = int(links[j].hull_index_first)
        hull_index_second = int(links[j].hull_index_second)

        dataset.append({"Name": name,
                        "HullIndexFirst": hull_index_first,
                        "HIF-ScaleX": hulls[hull_index_first].scale.x,
                        "HIF-ScaleY": hulls[hull_index_first].scale.y,
                        "HIF-ScaleZ": hulls[hull_index_first].scale.z,
                        "HIF-PositionX": hulls[hull_index_first].position.x,
                        "HIF-PositionY": hulls[hull_index_first].position.y,
                        "HIF-PositionZ": hulls[hull_index_first].position.z,
                        "HIF-OrientationW": hulls[hull_index_first].orientation.w,
                        "HIF-OrientationX": hulls[hull_index_first].orientation.x,
                        "HIF-OrientationY": hulls[hull_index_first].orientation.y,
                        "HIF-OrientationZ": hulls[hull_index_first].orientation.z,
                        "HullIndexSecond": hull_index_second,
                        "HIS-ScaleX": hulls[hull_index_second].scale.x,
                        "HIS-ScaleY": hulls[hull_index_second].scale.y,
                        "HIS-ScaleZ": hulls[hull_index_second].scale.z,
                        "HIS-PositionX": hulls[hull_index_second].position.x,
                        "HIS-PositionY": hulls[hull_index_second].position.y,
                        "HIS-PositionZ": hulls[hull_index_second].position.z,
                        "HIS-OrientationW": hulls[hull_index_second].orientation.w,
                        "HIS-OrientationX": hulls[hull_index_second].orientation.x,
                        "HIS-OrientationY": hulls[hull_index_second].orientation.y,
                        "HIS-OrientationZ": hulls[hull_index_second].orientation.z,
                        "Fitness": 1})

    return dataset

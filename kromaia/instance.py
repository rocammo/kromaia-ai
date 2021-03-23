from .util import config
from .util.config import log

from .entities.hull import Hull
from .entities.link import Link

from .model import model


def init(args):
    environment = config.get_config("kromaia.env.json", args.environment)
    log.verbose = environment["verbose"]


def run(args):
    init(args)

    hulls, links = model.parse_xml("objects/Vermis.xml")

    # Hulls.
    scales, positions, orientations = model.get_hulls_components(hulls)
    hulls_ = [Hull(scales[i], positions[i], orientations[i])
              for i in range(len(hulls))]
    for i in range(len(hulls)):
        log.vprint(f"{hulls_[i]}")
    log.vprint("")  # newline

    # Links.
    hull_index_first, hull_index_second = model.get_links_components(links)
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

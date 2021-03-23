from .util import config
from .util import io

from .util.config import log
from .util.colors import bcolors

from .model import model

from .lib import mutation


def init(args):
    global environment
    environment = config.get_config("kromaia.env.json", args.environment)
    log.verbose = environment["verbose"]


def do(action):
    if action in dispatch:
        dispatch[action]()
    else:
        log.vprint(
            f"{bcolors.FAIL}'{action}' is not valid action. Try with: {[key for key in dispatch.keys()]}.{bcolors.ENDC}\n")


def run(args):
    init(args)
    do(args.action)


def analyse(object):
    log.vprint(
        f"{bcolors.HEADER}{bcolors.UNDERLINE}objects/{object}.xml{bcolors.ENDC}\n")
    hulls, links = model.parse_xml(f"objects/{object}.xml")

    hulls_ = model.get_hulls(hulls)
    links_ = model.get_links(links)
    hulls_indexed = model.get_hulls_indexed_by_links(links_)

    return hulls_, links_


def mutate():
    objects = environment["objects"]

    for o in objects:
        hulls, links = analyse(o)

        dataset = model.to_dataset(f"{o}-baseline", hulls, links)
        io.export_dataset_to_csv(dataset, filename=f"{o}_dataset")

        mutation.mutate_model(dataset, props=environment["props"],
                              percentage=[10, 15], times=49,
                              filename=f"{o}_dataset_mut")

        log.vprint(
            f"{bcolors.OKGREEN}Done! Check generated dataset: {bcolors.ENDC}'{o}_dataset_mut.csv'.\n")


def train():
    pass


dispatch = {
    'data': mutate,
    'model': train
}

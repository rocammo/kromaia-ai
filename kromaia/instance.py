import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd

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
    workspace = environment["workspace"]

    for o in objects:
        hulls, links = analyse(o)

        dataset = model.to_dataset(f"{o}-baseline", hulls, links)
        io.export_dataset_to_csv(
            dataset, filename=f"{workspace}/datasets/{o}_dataset")

        mutation.mutate_model(dataset, props=environment["props"],
                              percentage=[10, 15], times=49,
                              filename=f"{workspace}/datasets/{o}_dataset_mut")

        log.vprint(
            f"{bcolors.OKGREEN}Done! Check generated dataset: {bcolors.ENDC}'./{workspace}/datasets/{o}_dataset_mut.csv'.\n")


def plot():
    objects = environment["objects"]
    workspace = environment["workspace"]

    for o in objects:
        log.vprint(
            f"{bcolors.HEADER}{bcolors.UNDERLINE}objects/{o}.xml{bcolors.ENDC}\n")
        model_data = pd.read_csv(f"{workspace}/datasets/{o}_dataset_mut.csv")

        # Summary statistics.
        summary_statistics = model_data.describe()
        log.vprint(summary_statistics, end='\n\n')

        # Classes.
        classes = "', '".join(model_data["Name"].unique())
        log.vprint(f"Classes: ['{classes}']", end='\n\n')

        # Plot.
        fig = plt.figure(figsize=(15, 9))
        fig.canvas.set_window_title(f"{o} model (HullIndexFirst)")

        discarded_columns_hif = ["Name", "HullIndexFirst",
                                 "HIF-OrientationW", "HIF-OrientationX", "HIF-OrientationY", "HIF-OrientationZ",
                                 "HullIndexSecond", "HIS-ScaleX", "HIS-ScaleY", "HIS-ScaleZ",
                                 "HIS-PositionX", "HIS-PositionY", "HIS-PositionZ", "HIS-OrientationW",
                                 "HIS-OrientationX", "HIS-OrientationY", "HIS-OrientationZ", "Fitness"]

        position = 0
        for column_index, column in enumerate(model_data.columns):
            if column in discarded_columns_hif:
                continue
            elif column == "HIF-PositionY":
                position += 1
                continue
            else:
                position += 1

            plt.subplot(2, 3, position)
            sb.violinplot(x="Name", y=column, data=model_data)

        # plt.show(block=False)
        plt.savefig(f"{workspace}/plots/{o}_model_HIF.pdf")
        log.vprint(
            f"{bcolors.OKGREEN}Check generated plot: {bcolors.ENDC}'./{workspace}/plots/{o}_model_HIF.pdf'.\n")

        fig = plt.figure(figsize=(15, 9))
        fig.canvas.set_window_title(f"{o} model (HullIndexSecond)")

        discarded_columns_his = ["Name", "HullIndexFirst",
                                 "HIF-ScaleX", "HIF-ScaleY", "HIF-ScaleZ",
                                 "HIF-PositionX", "HIF-PositionY", "HIF-PositionZ", "HIF-OrientationW",
                                 "HIF-OrientationX", "HIF-OrientationY", "HIF-OrientationZ",
                                 "HullIndexSecond", "HIS-OrientationX", "HIS-OrientationY",
                                 "Fitness"]

        position = 0
        positions = [1, 2, 3, 4, 5, 6, 7, 9]
        for column_index, column in enumerate(model_data.columns):
            if column in discarded_columns_his:
                continue

            plt.subplot(3, 3, positions[position])
            sb.violinplot(x="Name", y=column, data=model_data)

            position += 1

        # plt.show()
        plt.savefig(f"{workspace}/plots/{o}_model_HIS.pdf")
        log.vprint(
            f"{bcolors.OKGREEN}Check generated plot: {bcolors.ENDC}'./{workspace}/plots/{o}_model_HIS.pdf'.\n")

    # log.vprint(
    #     f"{bcolors.HEADER}{bcolors.UNDERLINE}objects/{o}.xml{bcolors.ENDC}\n")
    # model_data = pd.read_csv("Vermis_dataset_mut.csv")

    # sb.pairplot(model_data)
    # plt.show()


def train():
    objects = environment["objects"]
    workspace = environment["workspace"]

    # for o in objects:
    #     log.vprint(
    #         f"{bcolors.HEADER}{bcolors.UNDERLINE}objects/{o}.xml{bcolors.ENDC}\n")
    #     model_data = pd.read_csv(f"{o}_dataset_mut.csv")
    o = objects[3]
    log.vprint(
        f"{bcolors.HEADER}{bcolors.UNDERLINE}objects/{o}.xml{bcolors.ENDC}\n")
    model_data = pd.read_csv(f"{workspace}/datasets/{o}_dataset_mut.csv")

    all_inputs = model_data[["HIF-ScaleX", "HIF-ScaleY", "HIF-ScaleZ",
                             "HIF-PositionX", "HIF-PositionZ",
                             "HIS-ScaleX", "HIS-ScaleY", "HIS-ScaleZ",
                             "HIS-PositionX", "HIS-PositionY", "HIS-PositionZ",
                             "HIS-OrientationW", "HIS-OrientationZ"]].values
    all_classes = model_data["Name"].values
    log.vprint(all_inputs[:5])


dispatch = {
    'data': mutate,
    'plot': plot,
    'model': train
}

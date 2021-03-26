import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import warnings

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

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

    warnings.simplefilter(action='ignore', category=FutureWarning)


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
        plt.close("all")
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
        plt.close("all")
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
    log.vprint(all_inputs[:5], end='\n\n')
    log.vprint(all_classes, end='\n\n')

    (training_inputs,
     testing_inputs,
     training_classes,
     testing_classes) = train_test_split(all_inputs, all_classes, train_size=0.80, random_state=456)

    log.vprint(testing_inputs.shape, end='\n\n')

    ### DecisionTreeClassifier ###
    # Create the classifier.
    decision_tree_classifier = DecisionTreeClassifier()
    # Train the classifier on the training set.
    decision_tree_classifier.fit(training_inputs, training_classes)
    # Validate the classifier on the testing set using classification accuracy.
    log.vprint(decision_tree_classifier.score(
        testing_inputs, testing_classes))
    log.vprint(decision_tree_classifier.predict(
        testing_inputs[:1, :]), end='\n\n')

    ### RadiusNeighborsClassifier ###
    # Create the classifier.
    neigh = RadiusNeighborsClassifier(radius=2.0)
    # Train the classifier on the training set.
    neigh.fit(training_inputs, training_classes)
    # Validate the classifier on the testing set using classification accuracy.
    log.vprint(neigh.score(testing_inputs, testing_classes))
    log.vprint(neigh.predict(testing_inputs[:1, :]), end='\n\n')

    ### Model accuracies ###
    plt.title("Model accuracies")
    # DecisionTreeClassifier
    model_accuracies = []
    for repetition in range(1000):
        (training_inputs,
         testing_inputs,
         training_classes,
         testing_classes) = train_test_split(all_inputs, all_classes, train_size=0.75)

        decision_tree_classifier = DecisionTreeClassifier()
        decision_tree_classifier.fit(training_inputs, training_classes)
        classifier_accuracy = decision_tree_classifier.score(
            testing_inputs, testing_classes)
        model_accuracies.append(classifier_accuracy)
    sb.distplot(model_accuracies, label="DecisionTreeClassifier")
    # RadiusNeighborsClassifier
    model_accuracies = []
    for repetition in range(1000):
        (training_inputs,
         testing_inputs,
         training_classes,
         testing_classes) = train_test_split(all_inputs, all_classes, train_size=0.75)

        neigh = RadiusNeighborsClassifier(radius=2.0)
        neigh.fit(training_inputs, training_classes)
        classifier_accuracy = neigh.score(testing_inputs, testing_classes)
        model_accuracies.append(classifier_accuracy)
    sb.distplot(model_accuracies, label="RadiusNeighborsClassifier")
    plt.legend()
    # plt.show()
    plt.savefig(f"{workspace}/plots/{o}_model_accuracies.pdf")
    plt.close("all")

    '''
    The model achieves 97% classification accuracy without much effort.

    It's obviously a problem that our model performs quite differently depending on
    the subset of the data it's trained on. This phenomenon is known as overfitting:
    The model is learning to classify the training set so well that it doesn't gene-
    ralize and perform well on data it hasn't seen before.

    This problem is the main reason that most data scientists perform k-fold cross-validation
    on their models: Split the original data set into k subsets, use one of the subsets as the
    testing set, and the rest of the subsets are used as the training set. This process is then
    repeated k times such that each subset is used as the testing set exactly once.

    10-fold cross-validation is the most common choice.
    '''

    decision_tree_classifier = DecisionTreeClassifier()

    # cross_val_score returns a list of the scores, which we can visualize
    # to get a reasonable estimate of our classifier's performance
    cv_scores = cross_val_score(
        decision_tree_classifier, all_inputs, all_classes, cv=10)
    sb.distplot(cv_scores)
    plt.title('Average score: {}'.format(np.mean(cv_scores)))
    # plt.show()
    plt.savefig(f"{workspace}/plots/{o}_model_cv_scores.pdf")
    plt.close("all")


dispatch = {
    'data': mutate,
    'plot': plot,
    'model': train
}

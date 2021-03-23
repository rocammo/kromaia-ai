import random
import numpy as np

from kromaia.util import io
from kromaia.util.config import log


''' Subjects a given value to a mutation process.

The result of the mutation can be: (0) value incremented by a percent,
(1) value decremented by a percent, or (2) default value.

:param value: input value
:type value: float
:param percentage: mutation's percent
:type percentage: int
:returns: mutated value
:rtype: float
'''


def mutate_value(value: float, percentage: int) -> float:
    mutation = random.randrange(0, 2 + 1, 1)  # value range: (0, 1, 2)

    if mutation == 0:  # incremental mutation
        return float(value + value * (percentage / 100))
    elif mutation == 1:  # decremental mutation
        return float(value - value * (percentage / 100))
    else:
        return value


''' Subjects a given set of properties belonging to an specific dataset to a mutation process.

Usage:
  1. mutate_props(dataset_, props=props, percentage=[10, 15])
  2. mutate_props(dataset_, props=props, percentage=14)

:param dataset: input dataset
:type dataset: dictionary array
:param props: set of properties
:type props: str array
:param percentage: mutation's percent
:type percentage: int or list
:returns: mutated dataset
:rtype: dictionary array
'''


def mutate_props(dataset, props, percentage, index=0):
    if not isinstance(percentage, (int, list)):
        return

    dataset_mut = []

    isrange = True if isinstance(percentage, list) else False
    percentage_ = random.randrange(
        percentage[0], percentage[1] + 1, 1) if isinstance(percentage, list) else percentage

    for row in dataset:
        data = row.copy()

        if isrange:
            percentage_ = random.randrange(percentage[0], percentage[1] + 1, 1)

        for prop in props:
            # log.vprint(f"Link-{index}_{prop}: " +
            #            "{:.2f} -> ".format(row[prop]), end='')
            data[prop] = mutate_value(row[prop], percentage_)
            # log.vprint("{:.2f}".format(data[prop]) + f" ({percentage_}%)")

        data["Name"] = data["Name"].replace("baseline", "mutated")
        data["Fitness"] = 1 - percentage_ / 100
        # log.vprint(f"Link-{index}_Fitness: " +
        #            "{:.2f}\n".format(data["Fitness"]))

        dataset_mut.append(data)

        index += 1

    return dataset_mut


''' Subjects a given model to a mutation process.

:param dataset: input dataset
:type dataset: dictionary array
:param props: set of properties
:type props: str array
:param percentage: mutation's percent
:type percentage: int or list
:param times: number of times the mutation is performed (default: 1)
:type times: int
:param filename: name of the csv file where to export the dataset (default: None)
:type filename: str
'''


def mutate_model(dataset, props, percentage, times=1, filename=None):
    dataset_all = np.array(dataset[:])

    for t in range(times):
        dataset_mut = np.array(mutate_props(
            dataset[:], props, percentage))
        dataset_all = np.concatenate((dataset_all, dataset_mut))

    if filename is not None:
        io.export_dataset_to_csv(dataset_all, filename)

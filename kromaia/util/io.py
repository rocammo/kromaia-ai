import csv

from kromaia.util.config import log


def export_dataset_to_csv(dataset, filename):
    with open(filename + ".csv", mode='w') as file:
        fieldnames = ["Name",
                      "HullIndexFirst",
                      "HIF-ScaleX",
                      "HIF-ScaleY",
                      "HIF-ScaleZ",
                      "HIF-PositionX",
                      "HIF-PositionY",
                      "HIF-PositionZ",
                      "HIF-OrientationW",
                      "HIF-OrientationX",
                      "HIF-OrientationY",
                      "HIF-OrientationZ",
                      "HullIndexSecond",
                      "HIS-ScaleX",
                      "HIS-ScaleY",
                      "HIS-ScaleZ",
                      "HIS-PositionX",
                      "HIS-PositionY",
                      "HIS-PositionZ",
                      "HIS-OrientationW",
                      "HIS-OrientationX",
                      "HIS-OrientationY",
                      "HIS-OrientationZ",
                      "Fitness"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in dataset:
            # log.vprint(f"{row}\n")
            writer.writerow(row)

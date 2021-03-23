import argparse

from . import instance


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Exploring program synthesis in model-driven engineering "
                                     "through machine learning techniques in Kromaia scenario.")
    parser.add_argument("environment", metavar="environment", type=str,
                        help="run with environment (values: 'dev' or 'prod')")

    instance.run(args=parser.parse_args())

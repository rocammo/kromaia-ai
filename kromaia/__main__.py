import argparse

from . import instance


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Exploring program synthesis in model-driven engineering "
                                     "through machine learning techniques in Kromaia scenario.")
    parser.add_argument("environment", metavar="environment", type=str,
                        help="run with environment (values: 'dev' or 'prod')")

    rparser = parser.add_argument_group('required named arguments')
    rparser.add_argument("--action", type=str,
                         help="do action (values: 'data' or 'model')")

    instance.run(args=parser.parse_args())

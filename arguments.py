import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder",
        type=int,
        help="Number of partitions",
    )

    args = parser.parse_args()

    return args

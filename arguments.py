import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video_path",
        type=str,
        help="Path to the video",
    )
    parser.add_argument(
        "--folder_path",
        type=str,
        default=None,
        help="Path to the folder with videos",
    )

    args = parser.parse_args()

    return args

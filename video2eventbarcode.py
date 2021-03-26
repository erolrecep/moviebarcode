#!/usr/bin/env python


# import required libraries
import os
import time
import argparse
from src.eventbarcode import EventBarcode
from src.getVideoPaths import list_jsons


"""
    Test Cases:
     - Provide a list of barcode.json's and process eventbarcode generation
     - Provide a list of barcode.json path's and process eventbarcode generation
"""


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder",
                    help="json files path")

    args = vars(ap.parse_args())

    if args["folder"] is not None:
        if not os.path.exists(args["folder"]):
            raise ValueError("Provided json folder doesn't exist!")

        # project_home = os.getcwd()
        start = time.perf_counter()
        eb = EventBarcode(
            json_folder_path=args["folder"],
            # json_folder_path="output",
            barcode_width=5,
            # no_of_colors=5, verbose=True, criteria='random')
            no_of_colors=5,
            verbose=True,
            criteria='dominant'
        )
        eb.build(file_name="eventbarcode.png")
        stop = time.perf_counter()
        print(f"Total processing time is {stop-start }")


if __name__ == '__main__':
    main()

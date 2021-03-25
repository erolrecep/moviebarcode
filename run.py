#!/usr/bin/env python


# import required libraries
import os
import time
from src.eventbarcode import EventBarcode


"""
    Test Cases:
     - Provide a list of barcode.json's and process eventbarcode generation
     - Provide a list of barcode.json path's and process eventbarcode generation
"""


def main():
    project_home = os.getcwd()
    start = time.perf_counter()
    eb = EventBarcode(
        json_folder_path=project_home + "/output_aus",
        # json_folder_path="output",
        barcode_width=5,
        # no_of_colors=5, verbose=True, criteria='random')
        no_of_colors=5,
        verbose=True,
        criteria='dominant'
    )
    eb.build()
    stop = time.perf_counter()
    print(f"Total processing time is {stop-start }")


if __name__ == '__main__':
    main()

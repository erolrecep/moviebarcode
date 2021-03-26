#!/usr/bin/env python


# import required libraries
import argparse
import os
import time
import concurrent.futures
import numpy as np
from src.moviebarcode import Moviebarcode
from src.getVideoPaths import list_videos
from src.eventbarcode import EventBarcode


def vid2barcode(video_path):
    moviebarcode = Moviebarcode(video_path)
    moviebarcode.generate()
    # Create an image, .png file
    moviebarcode.make_image()
    # write to json file
    moviebarcode.write2json("output_aus/"+video_path.split("/")[-1].split(".")[0]+".json")


# Read user input video and generate moviebarcode out of it
def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
                    help="video file path")
    ap.add_argument("-p", "--path",
                    help="Path to the list of ")
    args = vars(ap.parse_args())

    if args["path"] is not None:
        if not os.path.exists(args["path"]):
            raise ValueError("Provided videos folder doesn't exist!")
        videos_paths = list(list_videos(args["path"]))

        # Multi-core (Multi-process) processing of a list of videos
        start = time.perf_counter()
        with concurrent.futures.ProcessPoolExecutor(max_workers=30) as executor:
            executor.map(vid2barcode, videos_paths)
        stop = time.perf_counter()
        print(f"[INFO] Total processing time: {stop - start:0.4f}")

    elif args["video"] is not None:
        start = time.perf_counter()
        vid2barcode(args["video"])
        stop = time.perf_counter()
        print(f"[INFO] Total processing time: {stop - start:0.4f}")
        # Eventbarcode processing
        ep = EventBarcode(json_folder_path="barcode.json")
        ep.load_all()
        print(np.array(ep.eventflow).astype('uint8'))
        ep.find_dominant_colors(content=np.array(ep.eventflow).astype('uint8'))
        print(ep.dominant_colors)


if __name__ == '__main__':
    main()

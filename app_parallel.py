#!/usr/bin/env python

# import required libraries
import cv2                                                                                     # opencv version is 3.3.1
import numpy as np
import os, sys
import argparse
import datetime
import pafy
import json
import pprint
import httplib2
import joblib


HOME = os.getcwd()
# # YTURL = "https://www.youtube.com/watch?v=g8vHhgh6oM0"
# output_directory = HOME + "/output" + "/" + YTURL.split("=")[-1]
# json_file = output_directory + "/" + YTURL.split("=")[-1] + ".json"
# png_file = output_directory + "/" + YTURL.split("=")[-1] + ".png"
#
#
# def validate_url(url):
#     c = httplib2.Http()
#     resp = c.request(YTURL, "HEAD")
#     return int(resp[0]["status"])

# This will be the accelerated version of master branch
# It will read youtube urls from a txt file and save movie_barcode as json file
# The critical think is we need to adjust all videos into the same lenght of json
# for the consistency.

# TODO: The purpose of this code is just creating a data set
# TODO: We should keep list of video ids within a csv file in case we want to measure the performance of clustering
# TODO: Do not forget to update the upstream project on github

# Read urls.txt and put them into an order of stream and generate movie_barcode
# Save each video into their own video id project folder
# For the visualization of clustering result, we can create a visualization of adding same cluster png's into a
# markdown and displat them together. So as a human, we can easily identify the similarities and differences of
# clusters.
# For numerically identification of clusters, we need another kind of measuring and visualization.


# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="Video path on your box")
# ap.add_argument("-l", "--verbose", default=1, help="display debug lines")
# ap.add_argument("-j", "--json", default=json_file, help="json file to write barcode data")
# ap.add_argument("-b", "--barcode", default=png_file, help="path to png file to write barcode image")
# ap.add_argument("-d", "--display", default=0, help="play video if you want to see")
# args = vars(ap.parse_args())


# TODO: add exception handling
def read_urls(filename):
    with open(filename, "r") as f:
        urls = f.read().split("\n")

    return urls


# TODO: With pafy, get list of video urls of youtube.
# TODO: return the list of videos within a playlist
def get_urls_from_playlist(playlist):
    return pafy.get_playlist(playlist)

#
# def frame_count(YTURL):
#     """
#     :param
#         YTURL: youtube video url -> it should be a single video.
#     :return:
#         number of frames in the video
#
#     :usage
#         n_frames = frame_count(YTURL)
#     """
#
#     video = cv2.VideoCapture(YTURL)
#
#     # if you have opencv 3 then call quick solution
#     if int(cv2.__version__.split(".")[0]) == 3:
#         if args["verbose"]:
#             print("[{} | INFO] Lucky! You have opencv 3.x version.".format(datetime.datetime.now().time()))
#         num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
#
#     else:
#         if args["verbose"]:
#             print("[{} | INFO] It seems you don't have opencv 3.x version.".format(datetime.datetime.now().time()))
#
#         num_frames = 0
#
#         while True:
#             # read frame-by-frame where the show begins!
#             ret, frame = video.read()
#             num_frames += 1
#
#     return num_frames


# TODO: return the generated movie barcode for a video url
def get_movie_barcode(url):
    # get url
    # get num of frames
    # get video object

    return 0


# the above code only takes the last link in the list.
# To get all links we need to parallelize it with joblib

def main():
    print("main function")

    # Parse all urls to links/video ids
    all_urls = read_urls("urls.txt")
    for url in all_urls:
        print(url)

    links = [get_urls_from_playlist(url) for url in all_urls]
    print(links["items"])

    # concatenate all links/video ids to a single list
    video_ids = []
    for link in links:
        print("Girdi")
        # print(link)
        # playlist = pafy.get_playlist(link)
        for video in link["items"]:
            video_ids += video["pafy"].videoid

    print(len(video_ids))

    # print("Number of videos in this play list: {}".format(len(playlist["items"])))

# with open("ids.txt", "w+") as f:
#     for video in playlist["items"]:
#         print("{} | {}".format(video['pafy'].videoid, video['pafy'].title))
#         f.write("{}\n".format(video['pafy'].videoid))


if __name__ == "__main__":
    main()
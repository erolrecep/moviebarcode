#!/usr/bin/env python


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

# TODO: Read the txt and add all urls into a pipeline
# TODO: add exception handling
def read_urls(filename):
    with open(filename, "r") as f:
        urls = f.read().split("\n")

    return urls


# TODO: With pafy, get list of video urls of youtube.
# TODO: return the list of videos within a playlist
def get_urls_from_playlist(playlist):
    return 0


# TODO: return the generated movie barcode for a video url
def get_movie_barcode(url):
    return 0


# TODO:

all_urls = read_urls("urls.txt")
for url in all_urls:
    print(url)
# import required libraries
import os
import time
import json
import logging
import concurrent.futures
from .getVideoPaths import list_jsons
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", level=logging.INFO)


"""
    Flow of the module
    1. Get path to the list of json files
    2. Read all these json files and calculate criteria for these json contents
        + Get the first frame average of all videos
        + Find the dominant colors on all videos and attach them one another based on the time
        + Select random frames average from each json file and put them together
        + Select particular time or frame from all input json files and stitch them together
    3. Delete json content from RAM and extend the eventflow array
    4. Complete looping all json files contents and complete the
    
    v0.0:
        - Serial processing
        - Provide a folder where all the input json files in it
        - Provide criteria for selecting which frames will be picked
        - Loop all json file contents and select the appropriate frame then stitch all the values into an array
        - Return this moviebarcode and display?
"""


# Define the HEX values of colours
def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


class EventBarcode:
    def __init__(self, json_folder_path, no_of_colors=5, verbose=True, criteria='dominant'):
        assert json_folder_path, str
        if not os.path.exists(json_folder_path):
            logging.error(msg=f"{json_folder_path} does not exist in the folder.")
        self.path = json_folder_path
        self.eventflow = []
        self.content = []
        self.criteria = criteria
        self.no_of_colors = no_of_colors
        self.dominant_colors = []
        self.verbose = verbose
        self.json_files = []

    def apply_criteria(self, content):
        if self.criteria == 'random':
            # find the length of the content and pick a random one
            leng_ = content.shape[0]
            self.eventflow.extend(content[np.random.choice(leng_)])
        elif self.criteria == 'first':
            self.eventflow.extend(content[0])
        elif self.criteria == 'dominant':
            self.eventflow.extend(self.find_dominant_colors(content))
        elif self.criteria == "middle":
            pass
        # TODO: think of adding another option for building the eventbarcode
        # Choose a specific time of all videos and attach particular frames
        # to do eventbarcode

    def get_json_files(self):
        self.json_files = list(list_jsons(basePath=self.path))

    def find_dominant_colors(self, content):
        # assert content, list

        # Calculate KMeans for the colors in the input barcode
        kmeans = KMeans(n_clusters=self.no_of_colors)
        labels = kmeans.fit_predict(content)

        counts = Counter(labels)
        counts = dict(sorted(counts.items()))

        center_colors = kmeans.cluster_centers_
        ordered_colors = [center_colors[i] for i in counts.keys()]
        hex_colours = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
        self.dominant_colors = [ordered_colors[i] for i in counts.keys()]

        if self.verbose:
            plt.pie(counts.values(), colors=hex_colours)
            plt.savefig("dominant_colors_pie.png")
            # plt.show()

    def load_json(self, json_file):
        with open(json_file) as f:
            content = json.load(f)
        # TODO: Apply criteria here and extend to eventflow array
        self.apply_criteria(content=content)
        # self.eventflow.extend(content)

    def load_all(self):
        for json_file in self.json_files:
            self.load_json(json_file=json_file)

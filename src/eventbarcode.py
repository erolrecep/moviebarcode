# import required libraries
import os
import json
import logging
import tqdm
from .getVideoPaths import list_jsons
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from .moviebarcode import Moviebarcode


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
    def __init__(self,
                 json_folder_path="output",
                 no_of_colors=5,
                 verbose=True,
                 criteria='random',
                 barcode_width=5
                 ):
        self.path = json_folder_path
        self.eventflow = []
        self.content = []
        self.criteria = criteria
        self.no_of_colors = no_of_colors
        self.dominant_colors = []
        self.verbose = verbose
        self.json_files = []
        self.barcode_width = barcode_width

    def get_json_files(self):
        """
        Get list of json files paths.
        """
        assert self.path, str
        if not os.path.exists(self.path):
            logging.error(msg=f"{self.path} does not exist in the folder.")
        self.json_files = list(list_jsons(basePath=self.path))

    def find_dominant_colors(self, content):
        """
        Finding dominant colors from the provided content.

        :param content: a list or list-like data structure

        :return: Nothing returns but the function result is a list of dominant RGB pixel values
        """

        # The content should be a list
        assert content, list

        # Filter out contents if the length of the content is smaller then or equal to number of colors
        if len(content) <= self.no_of_colors:
            self.dominant_colors = [[0, 0, 0] for idx in range(self.no_of_colors)]
        else:
            # Calculate KMeans for the colors in the input barcode
            kmeans = KMeans(n_clusters=self.no_of_colors)
            labels = kmeans.fit_predict(content)

            counts = Counter(labels)
            counts = dict(sorted(counts.items()))

            center_colors = kmeans.cluster_centers_
            ordered_colors = [center_colors[i] for i in counts.keys()]
            hex_colours = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
            self.dominant_colors = [ordered_colors[i] for i in counts.keys()]
            # self.dominant_colors.append(list(dominant_colors[0]))         # If we only want to the most dominant color

            if self.verbose:
                # In case to see the pie chart of the dominant colors
                plt.pie(counts.values(), colors=hex_colours)
                plt.savefig("output/dominant_colors_pie.png")
                plt.show()

    def apply_criteria(self, content):
        """
        For Eventbarcode generation, there are several methods.
        In this function, the criteria is determined

        :param content: a list or list-like data structure
        :return:
        """
        if self.criteria == 'random':
            # find the length of the content and pick a random one
            leng_ = len(content)
            print(f"Content length: {leng_}")
            self.eventflow.extend([content[np.random.choice(leng_)] for _ in range(self.barcode_width)])
        elif self.criteria == 'first':
            print(f"Criteria first")
            # self.eventflow.append(content[0])
            self.eventflow.extend([content[0] for _ in range(self.barcode_width)])
        elif self.criteria == 'dominant':
            print(f"Criteria dominant")
            self.find_dominant_colors(content)
            self.eventflow.extend(self.dominant_colors)
        # TODO: Calculate the middle frame and generate eventbarcode with this
        elif self.criteria == "middle":
            pass
        # TODO: Choose a specific time of all videos and attach particular frames to generate eventbarcode

    def build(
            self,
            file_name="eventbarcode.png",
            make_image=True
    ):
        """

        :param file_name: Provide the filename to record and name the output png file
                The default value is "eventbarcode.png"
        :param make_image: Create the image of the generated eventbarcode
                The default value is True. If it's False, save the eventbarcode as a json file.
        :return:
        """
        if len(self.json_files) == 0:
            self.get_json_files()
        print(f"All json files -> {self.json_files}")

        # Get dominant colors
        for json_file in tqdm.tqdm(self.json_files):
            print(json_file)
            with open(json_file) as f:
                content = json.load(f)
                # TODO: Set criteria here
                self.apply_criteria(content=content)

        # Generate moviebarcode out of all dominant colors
        mb = Moviebarcode(barcode_width=self.barcode_width)
        mb.generate(colors=self.eventflow)
        print(f"The length of eventbarcode {len(self.eventflow)}")

        if make_image:
            # save the resultant moviebarcode to the disk
            mb.make_image(file_name=os.getcwd()+"/"+self.criteria+"_aus_"+file_name)
        else:
            # TODO: Make sure the filename's file extension is .json
            mb.write2json(file_name=os.getcwd()+"/"+self.criteria+"_aus_"+file_name)

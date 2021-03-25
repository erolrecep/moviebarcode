# import required libraries
import os
import json
import logging
import numpy as np
import cv2
from imutils.video import FileVideoStream, FPS

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", level=logging.INFO)


class Moviebarcode:
    """
    Generate moviebarcode from an input video
    """
    # TODO: Optimize the resize process and rescale 1K+ size videos to 480
    def __init__(self, video_path=None, verbose=True,
                 # optimize=True                          # TODO: Work on to optimize the moviebarcode generation
                 barcode_width=1
                 ):
        self.video_path = video_path
        self.verbose = verbose
        self.generate_features = True                     # Generate input video specs such as fps, width, and height
        self.video = None
        self.fvs = None                                   # FVS object for accelerating video stream to threads
        self.frame_count = 0
        self.video_fps = 0                                # We get FPS value from OpenCV Flags
        self.video_width = None                           # We get width value from OpenCV Flags
        self.video_height = None                          # We get height value from OpenCV Flags
        self.frame_avgs = []                              # Raw pixel values of frame pixel averages
        self.elapsed_time = 0.0                           # Accelerated video queueing time
        self.processed_frame_count = 0                    # How many frames of video is processed in threaded process
        self.processed_video_width = 0                    # Final version of each frame processed width value
        self.processed_video_height = 0                   # Final version of each frame processed height value
        self.barcode_frame_count = 0                      # don't want to visualize all frames, change barcode_frequency
        self.barcode_frequency = None
        self.fps = 0                                      # We get this value from imutils' fps() function
        self.barcode = None                               # Keep barcode object for further use
        self.barcode_height = 224                         # Set barcode image height
        self.barcode_width = barcode_width

    def if_exist(self):
        """
        For provided video path, check if it exists

        :return: The result of if the video exists
        """
        if not os.path.exists(self.video_path):
            logging.info(msg=f"{self.video_path} doesn't exist!")
            return False
        return True

    def load_video(self):
        """
        Accelerated video stream with multi-threading support

        :return:
        """
        if self.verbose:
            logging.info(msg=f"{self.video_path} is loading ..")
        if self.if_exist():
            self.video = FileVideoStream(self.video_path)

    def get_frames_avgs(self):
        """
        Calculate frames' average pixel values for all frames of loaded video

        :return: build the list for average pixel values
        """
        if self.video is None:
            self.load_video()

        # Start video stream
        if self.verbose:
            logging.debug(msg=f"Video is being started ..")
        self.fvs = self.video.start()
        fps = FPS().start()

        # Generate video features before processing
        if self.generate_features:
            self.frame_count = int(self.video.stream.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_fps = int(self.video.stream.get(cv2.CAP_PROP_FPS))
            self.video_width = int(self.video.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(self.video.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

            if self.verbose:
                logging.info(msg=f"[Video] frame count: {self.frame_count}")
                logging.info(msg=f"[Video] FPS: {self.video_fps}")
                logging.info(msg=f"[Video] Size: {self.video_width} x {self.video_height}")

        # Loop frames in a while
        if self.verbose:
            logging.info(msg=f"Video frame average pixel values are being calculated ..")
        while self.fvs.more():
            frame = self.fvs.read()
            self.frame_avgs.append(cv2.mean(frame)[:3])
            fps.update()
        fps.stop()
        self.fvs.stop()

        # Generate video features after processing
        if self.generate_features:
            self.fps = int(fps.fps())
            self.elapsed_time = fps.elapsed()
            self.processed_frame_count = fps.elapsed() * fps.fps()
            self.processed_video_width = int(self.video_width)
            self.processed_video_height = int(self.video_height)
            if self.verbose:
                logging.info(msg=f"[Processed] frame count: {self.frame_count}")
                logging.info(msg=f"[Processed] FPS: {self.fps}")
                logging.info(msg=f"[Processed] Size: {self.processed_video_width} x {self.processed_video_height}")

    def get_barcode_frame_count(self):
        """
        Get the total number of frames for input video

        :return:
        """
        if self.barcode is not None:
            self.barcode_frame_count = self.barcode.shape[0]
        if self.verbose:
            logging.info(msg=f"Total number of frames in barcode: {self.barcode_frame_count}")

    def barcode_frame_sequence(self):
        """
        On moviebarcode generation, the sequence of frames average can be set

        :return: Setting the frequency with the user input
        """
        # per frame
        if self.barcode_frequency is None:
            self.barcode_frequency = 1

        # per second
        elif self.barcode_frequency == "second":
            self.barcode_frequency = self.fps

        # per n-frame
        elif "frames" in self.barcode_frequency:
            freq = self.barcode_frequency.split("frames")[0]
            if freq != int(freq):
                self.barcode_frequency = freq

        # per n-second
        elif "seconds" in self.barcode_frequency:
            freq = self.barcode_frequency.split("seconds")[0]
            if freq != int(freq):
                self.barcode_frequency = self.fps * freq

        # per minute
        elif self.barcode_frequency == "minute":
            self.barcode_frequency = self.fps * 60

        # per n-minute
        elif "minutes" in self.barcode_frequency:
            freq = self.barcode_frequency.split("minutes")[0]
            if freq != int(freq):
                self.barcode_frequency = self.fps * freq * 60

    def generate(self, colors=None):
        """
        Moviebarcode generation function.
        This function has options, if a list of pixel values are provided, the moviebarcode image can be generated
        :param colors: A list or list-like object that contains pixel values
        Default value is None

        :return: RGB image of generated moviebarcode
        """
        if colors is None:
            # generate frames average
            self.get_frames_avgs()
        else:
            self.frame_avgs = colors

        # TODO: Add barcode_frequency option to this assignment
        self.barcode = np.zeros((self.barcode_height, len(self.frame_avgs), 3), dtype="uint8")

        for (i, avg) in enumerate(np.array(self.frame_avgs)):
            cv2.rectangle(self.barcode,
                          (int(i*self.barcode_width), 0),
                          (int(i + 1)*self.barcode_width, self.barcode_height),
                          (int(avg[0]), int(avg[1]), int(avg[2])), 3)

        if self.verbose:
            logging.info(msg="Barcode is being calculated ...")

    # TODO: Make the barcode name dynamic to input video id
    def make_image(self, file_name="output/moviebarcode.png"):
        """
        Create the PNG RGB image for the barcode object.
        :param file_name: The filename to name and record the image.
        The default value is "output/moviebarcode.png"

        :return: Write RGB image to a PNG file.
        """
        # save as image
        if self.barcode is not None:
            cv2.imwrite(filename=file_name, img=self.barcode)
        else:
            self.generate()
            cv2.imwrite(filename=file_name, img=self.barcode)

    def display_barcode(self):
        """
        visualize the moviebarcode image with OpenCV
        :return:
        """
        if self.verbose:
            logging.info(msg="Barcode is displayed with OpenCV")
        cv2.imshow("Barcode", self.barcode)
        cv2.waitKey(0)

    # TODO: make json file name dynamic to input video id
    def write2json(self, file_name="output/barcode.json"):
        """
        Write moviebarcode pixel values to a json file
        :param file_name: Name the json file to record to the disk
        The default value is "output/barcode.json"
        :return:
        """
        # Since our values are OpenCV image object which is BGR imager, convert the moviebarcode array to RGB
        b = np.array(self.frame_avgs)[:, 0].reshape(-1, 1)
        g = np.array(self.frame_avgs)[:, 1].reshape(-1, 1)
        r = np.array(self.frame_avgs)[:, 2].reshape(-1, 1)
        self.frame_avgs = np.concatenate([r, g, b], axis=1)
        with open(file_name, "w") as json_file:
            json_file.write(json.dumps(self.frame_avgs.tolist()))
        if self.verbose:
            logging.info(msg="Barcode is being written to json file!")

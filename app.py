#!/usr/bin/env python3


import cv2                                                     # opencv version is 3.3.1
import numpy as np
import os, sys
import argparse
import datetime
import pafy
import json
import pprint


HOME = os.getcwd()
YTURL = "https://www.youtube.com/watch?v=g8vHhgh6oM0"
output_directory = HOME + "/output" + "/" + YTURL.split("=")[-1]
json_file = output_directory + "/" + YTURL.split("=")[-1] + ".json"
png_file = output_directory + "/" + YTURL.split("=")[-1] + ".png"


# Steps of the program
# 0- Command Line arguments for the program. Program will be app as well.
# 1- Check and validate the link is youtube link and is working
# 2- List available resolution and bitrate before stream
# 3- To stream, we need the best tool. Look for it.
# 4- Once we get the video object, start processing with opencv
# 5- To standardize the feature extraction part, we just need to determine output
# 6- Save movie barcode as json file first. Then we can process later on form of input data to ml model
# 7- Add new code for visualization part. Show some option other than as png file.


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Video path on your box")
ap.add_argument("-l", "--verbose", default=1, help="display debug lines")
ap.add_argument("-j", "--json", default = json_file, help="josn file to write barcode data")
ap.add_argument("-b", "--barcode", default=png_file, help="path to png file to write barcode image")
# ap.add_argument("-d", "--display", help="play video if you want to see")
args = vars(ap.parse_args())


# Check if output_directory is not available, create one
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    if args["verbose"]:
        print("[{} | INFO] Output directory is created.".format(datetime.datetime.now().time()))

else:
    if args["verbose"]:
        print("[{} | INFO] Output directory is already available.".format(datetime.datetime.now().time()))
    pass


#####################################################
### Link Validation and check whether it is alive ###
#####################################################


#################################################################
### We will use pafy, cv2, may be ffmpeg for video processing ###
#################################################################


# Steps for processing
# 1- find number of frames in video
# 2- get the video from youtube with pafy
# 3- generate movie barcode of the video with opencv
# 4- finalize the program and release the video


def frame_count(YTURL):
    """
    :param video: is an opencv VideoCapture() object
    :return:      number of frames in the video

    :usage
        cap = cv2.VideoCapture(movie.url)
        -> total=frame_count(cap)
    """

    # TODO: check if the video object is not empty

    video = cv2.VideoCapture(YTURL)

    # if you have opencv 3 then call quick solution
    if int(cv2.__version__.split(".")[0]) == 3:
        if args["verbose"]:
            print("[{} | INFO] Lucky! You have opencv 3.x version.".format(datetime.datetime.now().time()))
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    else:
        if args["verbose"]:
            print("[{} | INFO] It seems you don't have opencv 3.x version.".format(datetime.datetime.now().time()))

        num_frames = 0

        while True:
            # read frame-by-frame where the show begins!
            ret, frame = video.read()
            num_frames += 1

    return num_frames


def get_url(YTURL):
    video_pafy = pafy.new(YTURL)
    # TODO: We need to work on this a little bit
    best_specs = video_pafy.getbest(preftype="webm")

    # if args["verbose"]:
    #     print("[{} | INFO] YTURL: {}.".format(datetime.datetime.now().time(), best_specs.url))

    # TODO: print other information about video
    pp = pprint.PrettyPrinter(indent=2)

    print("-"*(len(video_pafy.title) + 18))
    print("| Video Title:    {}".format(video_pafy.title))
    print("| Video duration: {}".format(video_pafy.duration))
    print("| Video rating:   {}".format(video_pafy.rating))
    print("| Video author:   {}".format(video_pafy.author))
    print("| Video length:   {}".format(video_pafy.length))

    # print("| Video keywords: {}".format(video_pafy.keywords))            # if you would like to see keywords in a line

    # If you would like to visualize the object as dictionary
    # pprint.pprint(video_pafy, depth=1)

    print("| Video keywords:")
    pp.pprint(video_pafy.keywords)
    print("| Video thumb:    {}".format(video_pafy.thumb))
    print("| Video videoid:  {}".format(video_pafy.videoid))
    print("| Video viewcount:{}".format(video_pafy.viewcount))
    print("-"*(len(video_pafy.title) + 18))

    return best_specs.url


def generate_barcode(video):

    print("video object type: {}".format(type(video)))

    # mean value for each frame of the video
    avgs = []

    # TODO: check if the video object is not empty
    # TODO: Accelerate video streaming?
    while True:
        # get the frame
        (ret, frame) = video.read()

        if not ret:
            break

        frame_avg = cv2.mean(frame)[:3]
        avgs.append(frame_avg)

    if args["verbose"]:
        print("[{} | INFO] video barcode is ready. Size:{}".format(datetime.datetime.now().time(), len(avgs)))

    return avgs


def vis_barcode():
    # load the averages file and convert it to a NumPy array
    avgs = json.loads(open(args["json"]).read())
    np_avgs = np.array(avgs, dtype="int")

    # grab the individual bar width and allocate memory for
    # the barcode visualization
    bw = 1
    barcode = np.zeros((250, len(np_avgs) * bw, 3), dtype="uint8")

    # loop over the averages and create a single 'bar' for
    # each frame average in the list
    for (i, avg) in enumerate(np_avgs):
        # cv2.rectangle(barcode, (int(i * bw), 0), (int((i + 1) * bw), 250), tuple(avg), 3)
        cv2.rectangle(barcode, (int(i * bw), 0), (int((i + 1) * bw), 250), (int(avg[0]), int(avg[1]), int(avg[2])), 3)

    # write the video barcode visualization to file and then
    # display it to our screen
    cv2.imwrite(args["barcode"], barcode)
    cv2.imshow("Barcode", barcode)
    cv2.waitKey(0)
    if sys.platform == "linux":
        cv2.destroyAllWindows()


#######################################################
### movie barcode data will be saved as json object ###
#######################################################


def main():
    print("main")
    # print(cv2.getBuildInformation())

    video_url = get_url(YTURL=YTURL)
    num_frames = frame_count(video_url)

    video = cv2.VideoCapture(video_url)

    if args["verbose"]:
        print("[{} | INFO] Number of frames: {}".format(datetime.datetime.now().time(), num_frames))

    # Write barcode data to json file
    # Check if the file is already available, delete it.
    if not os.path.exists(args["json"]):
        with open(args["json"], "w") as json_file:
            json_file.write(json.dumps(generate_barcode(video=video)))
    else:
        os.remove(args["json"])
        with open(args["json"], "w") as json_file:
            json_file.write(json.dumps(generate_barcode(video=video)))

    video.release()

    if args["verbose"]:
        print("[{} | INFO] json file is being written to {}".format(datetime.datetime.now().time(), args["json"]))

    vis_barcode()


if __name__ == "__main__":
    main()

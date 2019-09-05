#!/usr/bin/env python3


import cv2                                                                                     # opencv version is 3.3.1
import numpy as np
import os, sys
import argparse
import datetime
import pafy
import json
import pprint
import httplib2


# TODO: check if youtube link is a video list
# TODO: Accelerate video streaming?

HOME = os.getcwd()
YTURL = "https://www.youtube.com/watch?v=g8vHhgh6oM0"
output_directory = HOME + "/output" + "/" + YTURL.split("=")[-1]
json_file = output_directory + "/" + YTURL.split("=")[-1] + ".json"
png_file = output_directory + "/" + YTURL.split("=")[-1] + ".png"


def validate_url(url):
    c = httplib2.Http()
    resp = c.request(YTURL, "HEAD")
    return int(resp[0]["status"])


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Video path on your box")
ap.add_argument("-l", "--verbose", default=1, help="display debug lines")
ap.add_argument("-j", "--json", default=json_file, help="json file to write barcode data")
ap.add_argument("-b", "--barcode", default=png_file, help="path to png file to write barcode image")
ap.add_argument("-d", "--display", default=0, help="play video if you want to see")
args = vars(ap.parse_args())


if validate_url(YTURL) == 200:
    if args["verbose"]:
        print("[{} | INFO] YouTube url is valid!.".format(datetime.datetime.now().time()))
else:
    raise ValueError("[{} | ERROR] YouTube url is not valid!.".format(datetime.datetime.now().time()))


# Check if output_directory is not available, create one
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    if args["verbose"]:
        print("[{} | INFO] Output directory is created.".format(datetime.datetime.now().time()))
else:
    if args["verbose"]:
        print("[{} | INFO] Output directory is already available.".format(datetime.datetime.now().time()))
    pass


def frame_count(YTURL):
    """
    :param
        YTURL: youtube video url -> it should be a single video.
    :return:
        number of frames in the video

    :usage
        n_frames = frame_count(YTURL)
    """

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
    """
    :param
        YTURL: youtube video url -> it should be a single video.
    :return:
        best available download link of the video

    :usage
        best_specs.url = get_url(YTURL)
    """

    video_pafy = pafy.new(YTURL)
    best_specs = video_pafy.getbest(preftype="webm")

    # if args["verbose"]:                                          # if you'd like to see the video url before download.
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
    """
    :param
        video: video object.
    :return:
        average R, G, B values of each frame in a video

    :usage
        avgs = generate_barcode(video)
    """

    if video is None:
        raise ValueError("[{} | ERROR] video object is empty!".format(datetime.datetime.now().time()))

    # mean value for each frame of the video
    avgs = []

    while True:
        # get the frame
        (ret, frame) = video.read()

        if not ret:
            break

        if args["display"]:
            cv2.imshow("video", frame)

        frame_avg = cv2.mean(frame)[:3]
        avgs.append(frame_avg)

    if args["verbose"]:
        print("[{} | INFO] video barcode is ready. Size:{}".format(datetime.datetime.now().time(), len(avgs)))

    return avgs


def vis_barcode():
    """
    :param
        None
    :return:
        None

    :usage
        Would you like to see the movie barcode on action?
    """

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


# Main function like we have in many C based languages
def main():
    print("main")
    # print(cv2.getBuildInformation())                                                # Display OpenCV build information

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

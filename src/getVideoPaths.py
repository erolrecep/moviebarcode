# import the necessary packages
import os

"""
    reference of this script: https://github.com/jrosebr1/imutils/blob/master/imutils/paths.py
"""


video_types = (".avi", ".mp4", ".webm", ".mkv")
json_type = (".json")


def list_videos(basePath, contains=None):
    # return the set of files that are valid
    return list_files(basePath, validExts=video_types, contains=contains)


def list_jsons(basePath, contains=None):
    return list_files(basePath, validExts=json_type, contains=contains)


def list_files(basePath, validExts=None, contains=None):
    # loop over the directory structure
    for (rootDir, dirNames, filenames) in os.walk(basePath):
        # loop over the filenames in the current directory
        for filename in filenames:
            # if the contains string is not none and the filename does not contain
            # the supplied string, then ignore the file
            if contains is not None and filename.find(contains) == -1:
                continue

            # determine the file extension of the current file
            ext = filename[filename.rfind("."):].lower()

            # check to see if the file is an image and should be processed
            if validExts is None or ext.endswith(validExts):
                # construct the path to the image and yield it
                imagePath = os.path.join(rootDir, filename)
                yield imagePath

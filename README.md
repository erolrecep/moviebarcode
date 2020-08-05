## Movie Barcode Generator


![movie_barcode_diagram](https://raw.githubusercontent.com/erolrecep/movie_barcode/master/images/movie_barcode_diagram.png)


### Usage

        $ (conda_env) python app.py
        
### Project Setup

Setup development environment with the provided *requirement.txt* file. However, due to TLS OpenSSL issue, you need to 
build *OpenCV* for your system. Then, add *.so* file to your virtualenv. If you're on OS X, you can install "opencv-contrib-python==4.0.0.21".

If you build opencv from it's source, 
for [linux](https://www.pyimagesearch.com/2018/08/15/how-to-install-opencv-4-on-ubuntu/), 
or for [Mac](https://www.pyimagesearch.com/2018/08/17/install-opencv-4-on-macos/) you can follow these steps;

        $ conda create --name moviebarcode
        $ conda activate moviebarcode
        $ (moviebarcode) conda install -r requirements.txt
        $ cd ~/miniconda3/envs/mb/lib/python3.x/site-packages/
        $ ln -s /usr/local/opencv/4.0.0/lib/python3.x/site-packages/cv2.so cv2.so # This file location may vary to operating systems.

To make sure, your system available to import opencv

        $ (movie_barcode) python
        $ >>> import cv2
        $ >>> print(cv2.getBuildInformation())
        $ # You should see build information for your opencv
        
I personally prefer to use [miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) for Python virtual environment management.

<br>

To use for [YouTube Public Data API](https://console.cloud.google.com/apis/), you need to create an API key. 
Then create a config file called _config.yaml_ and then create a placeholder called _key_.

<br>

### Expected Output

This sample project is implemented to see how movie_barcode idea works. The python script creates a folder called 
*/output*. YouTube link should be provided to run the script otherwise the default link is 
[Dilbert - The Knack "The Curse of the Engineer"](https://www.youtube.com/watch?v=g8vHhgh6oM0). Once the script runs, 
script requests the video for streaming and process the movie barcode generator. The video id will be 
experiment folder name and output file names.


        $ cd $PROJECT_HOME
        $ cd output
        $ tree .
        └── g8vHhgh6oM0
            ├── g8vHhgh6oM0.json
            └── g8vHhgh6oM0.png
            
            
for the image, you should see something like the below, if not, please check your internet connection first.

![g8vHhgh6oM0.png](https://github.com/erolrecep/movie_barcode/blob/master/images/g8vHhgh6oM0.png)


**This project is tested on Linux and OS X systems. If you think Windows systems worth to test, feel free to do it, but I highly recommend, do not try at home!**


**In case of emergency, there is a section in the toolbar called "issues", you can create one and github will 
send me the evacuation message. Thanks!**

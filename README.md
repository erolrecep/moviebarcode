## Movie Barcode Generator

### Usage

        $ (virtual_env)python app.py
        
### Project Setup

Setup development environment with the provided *requirement.txt* file. However, due to TLS OpenSSL issue, you need to 
build *OpenCV* for your system. Then, add *.so* file to your virtualenv.


        $ mkvirtualenv movie_barcode
        $ workon movie_barcode
        $ (movie_barcode) pip install -r requirements.txt
        $ cd ~/.virtualenvs/movie_barcode/lib/python3.x/site-packages/
        $ ln -s /usr/local/opencv/3.3.1/lib/python3.x/site-packages/cv2.so cv2.so

To make sure, your system available to import opencv

        $ (movie_barcode) python
        $ >>> import cv2
        $ >>> print(cv2.getBuildInformation())
        $ # You should see build information for your opencv
        
        
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

![g8vHhgh6oM0.png](https://github.com/erolrecep/movie_barcode/blob/master/img/g8vHhgh6oM0.png)




**In case of emergency, there is a section in the toolbar called "issues", you can create one and github will 
send me the evacuation message. Thanks!**

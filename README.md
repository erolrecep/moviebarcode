## Moviebarcode Generator


![movie_barcode_diagram](https://raw.githubusercontent.com/erolrecep/moviebarcode/moviebarcode/images/moviebarcode.gif)

        
### Project Setup

Create a Python virtual environment.

```shell
$ mkvirtualenv moviebarcode -p python3
```

Install required libraries
```shell
$ (moviebarcode) pip install -r requirements.txt
```

### Usage

Generate Moviebarcode with video2moviebarcode.py

```shell
$ (moviebarcode) python video2moviebarcode.py -v "video_path"
```

Use Moviebarcode module in your code

```python
from src.moviebarcode import Moviebarcode
moviebarcode = Moviebarcode(video_path=video_path)
moviebarcode.generate()
moviebarcode.display_barcode()
# Create an image, .png file
moviebarcode.make_image()
```

Sample barcode outputs

![g8vHhgh6oM0.png](https://raw.githubusercontent.com/erolrecep/moviebarcode/main/images/g8vHhgh6oM0.png)
![moviebarcode](https://raw.githubusercontent.com/erolrecep/moviebarcode/moviebarcode/images/moviebarcode.png)

Generate Eventbarcode with video2eventbarcode.py

```shell
$ (moviebarcode) python video2eventbarcode.py -f "json_files_path"
```

```python
from src.eventbarcode import EventBarcode
eb = EventBarcode(
            json_folder_path="json_files_path",
            barcode_width=5,
            no_of_colors=5,
            verbose=True,
            criteria='dominant'
        )
eb.build(file_name="eventbarcode.png")
```

Or

```python
from src.eventbarcode import EventBarcode
eb = EventBarcode(
            json_folder_path=None,
            barcode_width=5,
            no_of_colors=5,
            verbose=True,
            criteria='dominant'
        )
eb.json_files = [...] # Sorted list of json files to generate eventbarcode
eb.build(file_name="eventbarcode.png")
```


Sample Eventbarcode Images

![dominant_aus_eventbarcode.png]()
![first_aus_eventbarcode.png]()
![dominant_aus_eventbarcode.png]()

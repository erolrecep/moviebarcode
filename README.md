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

Generate Moviebarcode with main.py

```shell
$ (moviebarcode) python main.py -v "video_path"
```

Use Moviebarcode module in your code

```python
from src.moviebarcode import Moviebarcode
moviebarcode = Moviebarcode(video_path)
moviebarcode.generate()
moviebarcode.display_barcode()
# Create an image, .png file
moviebarcode.make_image()
```

Sample barcode outputs

![g8vHhgh6oM0.png](https://raw.githubusercontent.com/erolrecep/moviebarcode/main/images/g8vHhgh6oM0.png)
![moviebarcode](https://raw.githubusercontent.com/erolrecep/moviebarcode/moviebarcode/images/moviebarcode.png)

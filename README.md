## Moviebarcode Generator


![movie_barcode_diagram](https://raw.githubusercontent.com/erolrecep/moviebarcode/moviebarcode/images/moviebarcode.gif)

        
### Project Setup

Create a Python virtual environment.

```{shell}
mkvirtualenv moviebarcode -p python3
```

Install required libraries
```{shell}
(moviebarcode) pip install -r requirements.txt
```

### Usage

Generate Moviebarcode with main.py

```{shell}
(moviebarcode) python main.py -v "video_path"
```

Use Moviebarcode module in your code

```{python}
moviebarcode = Moviebarcode(video_path)
moviebarcode.generate()
# Create an image, .png file
moviebarcode.make_image()
moviebarcode.display_barcode()
```

![g8vHhgh6oM0.png](https://github.com/erolrecep/movie_barcode/blob/master/images/g8vHhgh6oM0.png)

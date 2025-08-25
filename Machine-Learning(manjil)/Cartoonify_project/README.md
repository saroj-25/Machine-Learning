## This is description about the project 

cartoonify.py → handles filtering

app.py → handles Flask routes

templates/ → HTML pages

static/css/ → CSS styling

static/uploads/ → uploaded + cartoonified images




## To make more cartoonify the given image i used the following module:

Color quantization (K-Means) :f lat painted colors

Edge detection  : black outlines

Bilateral smoothing + color boost : soft vibrant Ghibli look



## Model required for cartoonification

cv2 and numpy → ready-made modules (tools) you imported.

# function required for cartoonification in app.py

color_quantization() and cartoonify_image() → our own functions that use those tools to do cartoonification.
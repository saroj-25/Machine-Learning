# Object Tracking with Color (HSV Masking)

## Overview

This project demonstrates real-time object tracking using HSV color masking and Flask for web streaming. The object (e.g., a red ball) is tracked based on its color in the HSV color space.



## Folder Structure


- `app.py`: Flask application to stream video with tracked objects.
- `detection/color_tracker.py`: Contains the `ColorTracker` class for HSV-based tracking.
- `models/`: Directory to save and load tracker models.
- `templates/index.html`: HTML template for the Flask app.
- `requirements.txt`: List of Python dependencies.


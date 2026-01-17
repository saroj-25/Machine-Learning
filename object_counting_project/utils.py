import cv2
import numpy as np

def load_image(image_path):
    """Load image from path."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    return image

def preprocess_image(image):
    """Convert image to grayscale and blur."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    return blur

def get_contours_from_binary(binary_image):
    """Find contours in a binary image."""
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def filter_color(image, lower_hsv, upper_hsv):
    """Filter image by HSV color range."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    return mask

import cv2
import numpy as np
from utils import load_image, filter_color, get_contours_from_binary

IMAGE_PATH = "images/apple.jpg"
MIN_CONTOUR_AREA = 300  
PIXELS_PER_CM = 37     
DIST_THRESHOLD = 1 * PIXELS_PER_CM  
MIN_WIDTH_PX = 2 * PIXELS_PER_CM  
MIN_HEIGHT_PX = 2 * PIXELS_PER_CM 

# HSV Ranges (Red Apples)
COLOR_RANGES = {
    "Red": [((0, 70, 50), (10, 255, 255)), ((160, 70, 50), (179, 255, 255))]
}
BOX_COLORS = {"Green": (0, 255, 0)}

image = load_image(IMAGE_PATH)
image_blur = cv2.GaussianBlur(image, (5, 5), 0)
output = image.copy()

def rect_distance(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    dx = max(x2 - (x1 + w1), x1 - (x2 + w2), 0)
    dy = max(y2 - (y1 + h1), y1 - (y2 + h2), 0)
    return np.sqrt(dx*dx + dy*dy)

for color_name, ranges in COLOR_RANGES.items():
    mask = None
    for lower, upper in ranges:
        current_mask = filter_color(image_blur, lower, upper)
        mask = current_mask if mask is None else cv2.bitwise_or(mask, current_mask)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist, 0.4 * dist.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(mask, sure_fg)
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), markers)
    output[markers == -1] = [0, 255, 0]

    detected_boxes = []
    apple_count = 0
    unique_markers = np.unique(markers)
    for marker_id in unique_markers:
        if marker_id <= 1:
            continue
        mask_marker = np.uint8(markers == marker_id)
        contours = get_contours_from_binary(mask_marker)
        for contour in contours:
            if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
                continue
            x, y, w, h = cv2.boundingRect(contour)

            if w < MIN_WIDTH_PX or h < MIN_HEIGHT_PX:
                continue

            new_box = (x, y, w, h)

            if any(rect_distance(new_box, existing_box) < DIST_THRESHOLD for existing_box in detected_boxes):
                continue

            detected_boxes.append(new_box)
            apple_count += 1
            cv2.rectangle(output, (x, y), (x + w, y + h), BOX_COLORS['Green'], 2)
            cv2.putText(output, f"Apple-{apple_count}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, BOX_COLORS["Green"], 2)

    print(f"{color_name} apples detected: {apple_count}")

cv2.imshow("Original Image", image)
cv2.imshow("Detected Apples Individually", output)
cv2.waitKey(0)
cv2.destroyAllWindows()

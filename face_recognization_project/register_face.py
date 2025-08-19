'''
    Title: face Detection and Recognization Project
    features: 
     - User can feed their image
     - Store user images dataset/username/username1.png 
     - Later on we use that image for face recognization

'''

import cv2
import face_recognition
import os
import pickle

# get current directory of user
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print(BASE_DIR)


# dataset and encoding inside the project
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
ENCODING_FILE = os.path.join(BASE_DIR, "encodings.pkl")

# load dataset if already avaliable
if os.path.exists(ENCODING_FILE):
    with open(ENCODING_FILE, "rb") as f:
        known_encoding, known_name = pickle.load(f)
else:
    known_encoding, known_name = [], []


# get name from user
name = input("Enter your name: ")

# Create subfolder directory with username
user_dir = os.path.join(DATASET_DIR, name)

if not os.path.exists(user_dir):
    os.makedirs(user_dir)

cap = cv2.VideoCapture(1)
print("Enter c for capture and q for quit")
counter = 0

while True:
    ret, frame = cap.read()
    ## ret: Boolean result (True if frame captured successfully).
    ## frame: The actual image (numpy array).
    if not ret:  # if ret = false, not ret = true which means break! 
        print("Failed to capture frame")
        break
    cv2.imshow("Registerd frame",frame)
    key = cv2.waitKey(1) & 0xFF 
    if key == ord('c'):   # ord() function converts a character to ASCII integer for comparison.
        # recognize rgb value for face
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)    ## Detects faces, returns a list of bounding boxes ((T, R, B, L) coordinates).


        if (len(boxes)==0):
            print("No face detected, try again!")
            continue
        
        for box in boxes:
            top, right, bottom, left = box
            face_img = frame[top:bottom, left:right]


        # save the face inside folder
        filepath = os.path.join(user_dir,f"{name}_{counter}.png")
        cv2.imwrite(filepath, face_img)


        # Converts face into a 128-dimensional numerical vector (machine-readable format).
        encodings = face_recognition.face_encodings(rgb, [box])
        if encodings:
            known_encoding.append(encodings[0])  # Add face encoding
            known_name.append(name)            # Add corresponding name
            print(f"Saved face {counter} for {name}")
        counter += 1
    elif key == ord("q"):
        break


# Release webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()



# Save all encodings and names to a file for future use
with open(ENCODING_FILE, "wb") as f:
    pickle.dump((known_encoding, known_name), f)


print("Encoding done and save inside project folder")


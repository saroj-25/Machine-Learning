''' 
Title : Face Detection and Recognition Project
Features: 
- User can feed their image 
- Store user images dataset/username/username1.png (File handling)
- Later on we use that image for face recognition 
'''

import cv2
import face_recognition 
import os
import pickle
import numpy as np

#get current directory of user
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

#dataset and encoding inside the project
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
ENCODING_FILE = os.path.join(BASE_DIR, "encodings.pkl")

#load data set if already available
if os.path.exists(ENCODING_FILE):
    with open(ENCODING_FILE, "rb") as f:
        known_encoding, known_name = pickle.load(f)
else:
    known_encoding, known_name = [], []

# get name from user  
name = input("Enter your name: ")  

#create subfolder directory with username
user_dir = os.path.join(DATASET_DIR, name)
if not os.path.exists(user_dir):
    os.makedirs(user_dir)

cap = cv2.VideoCapture(0)   # if issues on Windows: cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("Enter c for capture and q for quit")
counter = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Register frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        # --- Strict conversion for face_recognition ---
        if frame is None:
            print("Empty frame, skipping.")
            continue

        # Drop alpha if present
        if len(frame.shape) == 3 and frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # Convert BGR -> RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Ensure contiguous uint8
        rgb = np.ascontiguousarray(rgb, dtype=np.uint8)

        print("Image dtype:", rgb.dtype)
        print("Image shape:", rgb.shape)

        # Detect faces
        boxes = face_recognition.face_locations(rgb)
        print("Boxes:", boxes)

        if len(boxes) == 0:
            print("No face Detected , Try Again!!!")
            continue

        for box in boxes:
            top, right, bottom, left = box 
            face_img = frame[top:bottom, left:right]

            # save the face inside your folder 
            filepath = os.path.join(user_dir, f"{name}_{counter}.jpg")
            cv2.imwrite(filepath, face_img)

            # encode face
            encodings = face_recognition.face_encodings(rgb, [box])
            if encodings:
                encoding = encodings[0]
                known_encoding.append(encoding)
                known_name.append(name)
                print(f"saved face {counter} for {name}")
            else:
                print("Skipping encoding process")

            counter += 1  

    elif key == ord('q'):
        break    

cap.release()
cv2.destroyAllWindows()

#save encoding inside project 
with open(ENCODING_FILE, 'wb') as f:
    pickle.dump((known_encoding, known_name), f)
print("Encoding done and set inside project folder.")    

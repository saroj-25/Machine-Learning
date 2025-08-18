'''
    Title: Face detection and recognization project
    Features: 
        - User can feed their image
        - Store user images dataset/username/username1.png (File handling)
        - Later on we use that image for face recognization
'''
import cv2
import face_recognition
import os
import pickle

#get current directory of user
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)


#dataset and encoding inside the project 
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
ENCODING_FILE = os.path.join(BASE_DIR,"encodings.pkl")

#load dataset if already available
if os.path.exists(ENCODING_FILE):
    with open(ENCODING_FILE,"rb") as f:
        known_encoding, known_name= pickle.load(f)
else: 
    known_encoding,known_name=[],[]

# get name from user
name = input ("Enter your name: ")


# crate subfolder directory with username 
user_dir = os.path.join(DATASET_DIR,name)

if not os.path.exists(user_dir):
    os.makedirs(user_dir)

# capture video
cap= cv2.VideoCapture(1)

print ("Enter c for capture and q for quit")

counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("failed to capture frame")
        break
    cv2.imshow("Register frame,", frame)


    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        #recognize rgb value for face
        rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        boxes = face_recognition.face_locations(rgb)


        if (len(boxes)==0):
            print("No face detected try again")
            continue

        for box in boxes:
            top, right ,bottom,left = box
            face_img = frame[top:bottom,left:right]
        
        # Save the face inside your folder 
        filepath = os.path.join(user_dir,f"{name}_{counter}.jpg")
        cv2.imwrite(filepath,face_img)


        # Encode face
        encodings = face_recognition.face_encodings(rgb,[box])
        if encodings:
            known_encoding.append(encodings[0])
            known_name.append(name)
            print(f"Saved face {counter} for {name}")
        counter+=1
    
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# save encoding inside project
with open(ENCODING_FILE,'wb') as f:
    pickle.dump((known_encoding,known_name),f)

print("Encoding done and save inside project folder")


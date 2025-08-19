import cv2
import os
import face_recognition


# get the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# data set
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')


# 1. load all the data from the dataset
known_encodings= [] 
known_names= []

for user_name in os.listdir(DATASET_DIR):
    user_folder= os.path.join(DATASET_DIR, user_name)

    if not os.path.isdir(user_folder):
        continue

    for file_name in os.listdir(user_folder):
        filepath= os.path.join(user_folder, file_name)
        image= face_recognition.load_image_file(filepath)
        encodings= face_recognition.face_encodings(image)


        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(user_name)


print("Loading data from the dataset process completed...")


#start webcam
cap= cv2.VideoCapture(1)
if not cap.isOpened():
    raise IOError("Cannot open webcam")


print("Enter q for quit")

while True:
    ret,frame= cap.read()
    
    if not ret:
        continue

    rgb= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    #Detect Face
    boxes= face_recognition.face_locations(rgb)
    encodings= face_recognition.face_encodings(rgb, boxes)

    names= []

    for encoding in encodings:
        matches= face_recognition.compare_faces(known_encodings, encoding, tolerance= 0.5)


        name= "Unknown"

        if True in matches:
            matched_idxs= [i for i, b in enumerate(matches) if b]
            counts= {}
            for i in matched_idxs:
                counts[known_names[i]]= counts.get(known_names[i], 0)+ 1
            
            if counts:
                name= max(counts, key= counts.get)
                #names.append(name)
        names.append(name)

    #draw rectangle on faces
    for ((top, right, bottom, left), names) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255, 0))


        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255,255), 2)
    
    cv2.imshow("Face Recognization", frame)
    
    if cv2.waitKey(1) & 0xFF ==  ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
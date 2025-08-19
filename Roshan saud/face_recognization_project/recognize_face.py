import cv2
import os
import recognize_face
import face_recognition

# get the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# data set
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')


# 1. load all the data from the dataset
known_encoding = [] 
known_names = []

for user_name in os.listdir(DATASET_DIR):
    user_folder = os.path.join(DATASET_DIR, user_name)

    if not os.path.isdir(user_folder):
        continue
    
    for file_name in os.listdir(user_folder):
        filepath = os.path.join(user_folder, file_name)
        image = face_recognition.load_image_file(filepath)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encoding.append(encodings[0])
            known_names.append(user_name)


print("Loading data from the dataset process completed!!! ")


# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened:
    raise ImportError("Cannot open webcam")

print("Enter q for quit:")

# while True:
#     ret, frame = cap.read()

#     if not ret:
#         continue

#     rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

#     # Detect face 
#     boxes = face_recognition.face_locations(rgb)
#     encodings = face_recognition.face_encodings(rgb, boxes)

#     names = [] 

#     for encoding in encodings:
#         matches = face_recognition.compare_faces(known_encoding, encoding)

#         name = 'Unknown'
#         if True in matches:
#             matched_idxs = [i for i, b in enumerate(matches) if b]
#             counts = {}
#             for i in matched_idxs:
#                 name = known_names[i]
#                 counts[name] = counts.get(name, 0) +  1
            
#             if counts:
#                 name = max(counts, key=counts.get)
#                 names.append(name)

    
#     # Draw rectangle on faces 
#     for((top, right, bottom, left), name) in zip(boxes, names):
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#         cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

    

#     cv2.imshow("Face recognition", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
        # break

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert to RGB for face_recognition
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces & encode
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(known_encoding, encoding, tolerance=0.5)  # stricter tolerance
        name = "Unknown"

        if True in matches:
            matched_idxs = [i for i, b in enumerate(matches) if b]
            counts = {}
            for i in matched_idxs:
                counts[known_names[i]] = counts.get(known_names[i], 0) + 1

            if counts:  # only if we have at least one match
                name = max(counts, key=counts.get)

        names.append(name)

    # Draw results
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Face recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break











cap.release()
cv2.destroyAllWindows()




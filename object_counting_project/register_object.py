import cv2
import os
import pickle

#get current directory of the user
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print (BASE_DIR)

#dataset and encoding inside the project
DATASET_DIR = os.path.join(BASE_DIR,"dataset1")
ENCODING_FILE = os.path.join(BASE_DIR,"encoding.pkl")

#load dataset if already available
if os.path.exists(ENCODING_FILE):
    with open(ENCODING_FILE,"ra") as o:
        known_encoding, known_name= pickle.load(o)
else: 
    known_encoding,known_name=[],[]

#get which object needed to be counted by user
name = input("Enter the object name :")

#create subfolder directory with the respective data's name 
object_dir = os.path.join(DATASET_DIR,name)
if not os.path.exists(object_dir):
    os.mkdir(object_dir)


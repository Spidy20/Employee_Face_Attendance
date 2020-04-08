# import cv2
# import numpy as np
# from PIL import Image
# import os
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#
# def getImagesAndLabels(path):
#     imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
#     # create empth face list
#     faceSamples = []
#     # create empty ID list
#     Ids = []
#     # now looping through all the image paths and loading the Ids and the images
#     for imagePath in imagePaths:
#         # loading the image and converting it to gray scale
#         pilImage = Image.open(imagePath).convert('L')
#         # Now we are converting the PIL image into numpy array
#         imageNp = np.array(pilImage, 'uint8')
#         # getting the Id from the image
#
#         Id = int(os.path.split(imagePath)[-1].split(".")[1])
#         # extract the face from the training image sample
#         faces = detector.detectMultiScale(imageNp)
#         # If a face is there then append that in the list as well as Id of it
#         for (x, y, w, h) in faces:
#             faceSamples.append(imageNp[y:y + h, x:x + w])
#             Ids.append(Id)
#     return faceSamples, Ids
#
# try:
#     os.mkdir("TrainingImageLabel")
#     faces, Id = getImagesAndLabels("TrainingImage")
#     recognizer.train(faces, np.array(Id))
#     recognizer.save("./TrainingImageLabel/Trainner.yml")
# except Exception as e:
#     print(e)

import csv

names = ['kisha' ,'smith'  , 'kishasmith@gmail.com', 40000  ,  '1-1-2029'   ,'janitor' ]
fieldnames2 = ['fir' , 'last' , 'email' , 'salary' , 'DOB' , 'occupation']

# for creating the dictionary object mapping "names" and "fieldnames2"
my_names_dict = dict(zip(fieldnames2, names))

with open('my_file.csv' , 'a+')as employee_file:
     csvwriter = csv.DictWriter(employee_file , fieldnames = fieldnames2 , delimiter = ',')
     csvwriter.writeheader()
     csvwriter.writerow(my_names_dict)
# import cv2
# import numpy as np
# from PIL import Image
# import os
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#
# def getImagesAndLabels(path):
#     imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
#     faceSamples = []
#     Ids = []
#     for imagePath in imagePaths:
#         pilImage = Image.open(imagePath).convert('L')
#         imageNp = np.array(pilImage, 'uint8')
#         Id = int(os.path.split(imagePath)[-1].split(".")[1])
#         faces = detector.detectMultiScale(imageNp)
#         for (x, y, w, h) in faces:
#             faceSamples.append(imageNp[y:y + h, x:x + w])
#             Ids.append(Id)
#     return faceSamples, Ids
#
# try:
#     os.mkdir("Trained_model")
#     faces, Id = getImagesAndLabels("TrainingImage")
#     recognizer.train(faces, np.array(Id))
#     recognizer.save("./Trained_model/Model.yml")
# except Exception as e:
#     print(e)
from tkinter import *
root = Tk()
frames = [PhotoImage(file='./images/play.gif',format = 'gif -index %i' %(i)) for i in range(8)]
def update(ind):
    frame = frames[ind]
    ind += 1
    print(ind)
    if ind>7:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)

label = Label(root,borderwidth=0,bg = 'white')
label.pack()
root.after(0, update, 0)
root.mainloop()
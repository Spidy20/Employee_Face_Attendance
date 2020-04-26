from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Progressbar
import tkinter as tk
from PIL import ImageTk,Image
import cv2
import numpy as np
import datetime,subprocess
import pyttsx3
import time,csv,os
from pathlib import Path
import time

#Size for displaying Image
w = 500;h = 360
size = (w, h)

windo = Tk()
windo.configure(background='white')
windo.title("EAFR: Employee Attendance using Face\ud83d\ude00 Recogntion")
width  = windo.winfo_screenwidth()
height = windo.winfo_screenheight()
windo.geometry(f'{width}x{height}')
windo.iconbitmap('./images/app.ico')
windo.resizable(0,0)
s = 0
##AUdio initialization
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def image_generate():
    global dn,imageFrame,display,id,name,cam
    id = id_txt.get()
    name = name_txt.get()
    re = Path('TrainingImage')
    if re.is_dir():
        pass
    else:
        os.mkdir('TrainingImage')
    if id == '' or name == '':
        ict = tk.Label(windo, text="Please Enter Following....", width=22, height=1, fg="black", bg="yellow",
                      font=('times', 14, ' bold '))
        ict.place(x=280, y=247)
        windo.after(5000, destroy_widget, ict)
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            imageFrame = tk.Frame(windo)
            imageFrame.place(x=665, y=53)
            display = tk.Label(imageFrame)
            display.grid()

            imageFrame1 = tk.Frame(windo)
            imageFrame1.place(x= 30, y=88)

            display1 = tk.Label(imageFrame1, borderwidth = 6,highlightbackground='yellow')
            display1.grid()

            ip = tk.Label(windo, text= name, width=14, height=1, fg="black", bg="yellow",
                          font=('times', 18, ' bold '))
            ip.place(x=30, y=260)
            def test():
                global s,x,y,w,h,gray,g,ic
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 6)
                    s = s + 1
                    print(s)
                    cv2.imwrite("./TrainingImage/ " + name + "." + id + '.' + str(s) + ".jpg",
                                gray[y:y + h, x:x + w])
                    ic = tk.Label(windo, text="Image Count: " + str(s+1), width=13, height=1, fg="black", bg="yellow",
                                  font=('times', 14, ' bold '))
                    ic.place(x=280, y=247)
                    gm = Image.fromarray(gray[y:y + h, x:x + w])
                    gm = gm.resize((190, 187), Image.ANTIALIAS)
                    imgtk1 = ImageTk.PhotoImage(image=gm)
                    display1.imgtk = imgtk1
                    display1.configure(image=imgtk1)
                    if s>29:
                        ic.destroy()
                        break
                cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
                rgb = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
                img = Image.fromarray(rgb)
                img = img.resize(size, Image.ANTIALIAS)
                imgtk = ImageTk.PhotoImage(image=img)
                display.imgtk = imgtk
                display.configure(image=imgtk)
                k = display.after(10, test)
                if s>29:
                    display.after_cancel(k)
                    s = 0
                    windo.after(3000,destroy_widget,ic)
                    windo.after(2000, destroy_widget, imageFrame)
                    windo.after(2000, destroy_widget, display)
                    windo.after(2000, destroy_widget, imageFrame1)
                    windo.after(2000, destroy_widget, display1)
                    windo.after(2000, destroy_widget, ip)
                    speak('Thank you ' + name + ', Your Face Data is Captured')
                    breakcam()
            test()
            my_file = Path("./RegisteredEmployees/RegisteredEmployees.csv")
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [id, name, Date, Time]
            head = ['Employye ID', 'Name', 'Date', 'Registration Time']
            dir2 = Path('RegisteredEmployees')
            if dir2.is_dir():
                pass
            else:
                os.mkdir('RegisteredEmployees')
            if my_file.is_file():
                print('file exists')
                row = [id, name, Date, Time]
                with open('./RegisteredEmployees/RegisteredEmployees.csv', 'a+',newline="") as csvFile:
                    writer = csv.writer(csvFile, delimiter=',')
                    writer.writerow(row)
                    csvFile.close()
            else:
                print('FIle not available')
                wrinting = dict(zip(head, row))
                with open('./RegisteredEmployees/RegisteredEmployees.csv', 'a+',newline="") as csvFile:
                    writer = csv.DictWriter(csvFile, delimiter=',', fieldnames=head)
                    writer.writeheader()
                    writer.writerow(wrinting)
                    csvFile.close()
        except Exception as e:
            ict = tk.Label(windo, text="Something went wrong....", width=22, height=1, fg="black", bg="yellow",
                           font=('times', 14, ' bold '))
            ict.place(x=280, y=247)
            windo.after(6000, destroy_widget, ict)
            windo.after(1000, destroy_widget, dn)
            windo.after(1000, destroy_widget, imageFrame)
            windo.after(1000, destroy_widget, display)
            windo.after(1000, destroy_widget, imageFrame1)
            windo.after(1000, destroy_widget, display1)
            windo.after(1000, destroy_widget, ip)
            speak('Something is wrong')
            print(e)

def model_training():
    try:
        os.remove("./Trained_model/Model.yml")
    except:
        pass
    def getImagesAndLabels(path):
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        Ids = []
        for imagePath in imagePaths:
            pilImage = Image.open(imagePath).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(imageNp)
            for (x, y, w, h) in faces:
                faceSamples.append(imageNp[y:y + h, x:x + w])
                Ids.append(Id)
        return faceSamples, Ids
    def gen_lab():
        ic1 = tk.Label(windo, text="Model Trained..", width=13, height=1, fg="black", bg="yellow",
                       font=('times', 14, ' bold '))
        ic1.place(x=280, y=247)
        windo.after(4000, destroy_widget, ic1)

    def bar():
        import time
        progress['value'] = 20
        windo.update_idletasks()
        time.sleep(1)
        progress['value'] = 40
        windo.update_idletasks()
        time.sleep(1)
        progress['value'] = 60
        windo.update_idletasks()
        time.sleep(1)
        progress['value'] = 80
        windo.update_idletasks()
        time.sleep(1)
        progress['value'] = 100
        windo.update_idletasks()
        progress.destroy()
        windo.after(10, gen_lab)

    progress = Progressbar(windo, orient=HORIZONTAL, length=100, mode='determinate')
    progress.place(x=280, y=247)
    bar()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Id = getImagesAndLabels("TrainingImage")
    qw = Path('Trained_model')
    if qw.is_dir():
        pass
    else:
        os.mkdir('Trained_model')
    recognizer.train(faces, np.array(Id))
    recognizer.save("./Trained_model/Model.yml")
    # windo.after(8000,destroy_widget,gif_play)

def destroy_widget(widget):
    widget.destroy()
def breakcam():
    cam.release()
#
# def admin_panel():
#     sg_f.destroy()
#     ca.destroy()
#     t_m.destroy()
#     tb.destroy()
#
#     panel41 = Label(windo, image=sad_img)
#     panel41.pack()
#     panel41.place(x=0, y=50)
#
#     start1 = tk.Label(windo, text="Please Enter your Adminstrator Details here!", bg="yellow", fg="black",
#                       width=35,
#                       height=1, font=('times', 20, 'bold '))
#     start1.place(x=0, y=50)
#
#     id_l = tk.Label(windo, text="Enter Username", width=13, height=1, fg="white", bg="midnightblue",
#                     font=('times', 14, ' bold '))
#     id_l.place(x=280, y=98)
#
#     def limitSizeid(*args):
#         value = idValue.get()
#         if len(value) > 8: idValue.set(value[:8])
#
#     idValue = StringVar()
#     idValue.trace('w', limitSizeid)
#
#     def limitSizename(*args):
#         value1 = nameValue.get()
#         if len(value1) > 12: nameValue.set(value1[:12])
#
#     nameValue = StringVar()
#     nameValue.trace('w', limitSizename)
#
#     def clear_id():
#         id_txt.delete(first=0, last=10)
#
#     def clear_name():
#         name_txt.delete(first=0, last=15)
#
#     id_txt = tk.Entry(windo, width=13, bg="white", fg="black", font=('times', 22, ' bold '), textvariable=idValue)
#     id_txt.place(x=280, y=125)
#
#     name_l = tk.Label(windo, text="Enter Password", width=13, height=1, fg="white", bg="midnightblue",
#                       font=('times', 14, ' bold '))
#     name_l.place(x=280, y=175)
#
#     name_txt = tk.Entry(windo, width=13, bg="white", fg="black", font=('times', 22, ' bold '), textvariable=nameValue)
#     name_txt.place(x=280, y=202)
#
#     clearButton = tk.Button(windo, command=clear_id, text="Clear", fg="white", bg="midnightblue", width=5, height=1,
#                             activebackground="yellow", font=('times', 12, ' bold '))
#     clearButton.place(x=490, y=127)
#
#     clearButton1 = tk.Button(windo, command=clear_name, text="Clear", fg="white", bg="midnightblue", width=5, height=1,
#                              activebackground="yellow", font=('times', 12, ' bold '))
#     clearButton1.place(x=490, y=204)
#
#     sub = tk.Button(windo, text="Submit", fg="white", bg="midnightblue",
#                    width=18, height=1, activebackground="yellow", font=('times', 18, ' bold '))
#     sub.place(x=280, y=290)
#
#     back = tk.Button(windo,command = go_back, text="Go Back", fg="white", bg="midnightblue", width=18,
#                    height=1, activebackground="yellow", font=('times', 18, ' bold '))
#     back.place(x=280, y=350)
#
# def go_back():
#     sg1 = PhotoImage(file="./images/cartoon.png")
#     sg_f1 = tk.Button(windo, borderwidth=0, image=sg1, bg='white', command=image_generate)
#     sg_f1.place(x=50, y=480)
#
#     ca1 = tk.Label(windo, text="Generate Faces", bg="midnightblue", fg="white", width=11,
#                   height=1, font=('times', 16, 'italic bold '))
#     ca1.place(x=48, y=590)
#
#     tm1 = PhotoImage(file="./images/train.png")
#     t_m1 = tk.Button(windo, borderwidth=0, bg='white', image=tm1, command=model_training)
#     t_m1.place(x=250, y=480)
#
#     tb1 = tk.Label(windo, text="Train Model", bg="midnightblue", fg="white", width=11,
#                   height=1, font=('times', 16, 'italic bold '))
#     tb1.place(x=248, y=587)

sad_img = ImageTk.PhotoImage(Image.open("./images/t1.jpg"))
panel4 = Label(windo, image=sad_img)
panel4.pack()
panel4.place(x=0, y=50)

id_l = tk.Label(windo, text="Enter ID", width=13, height=1, fg="white", bg="midnightblue", font=('times', 14, ' bold '))
id_l.place(x=280, y=98)

def limitSizeid(*args):
    value = idValue.get()
    if len(value) > 8: idValue.set(value[:8])

idValue = StringVar()
idValue.trace('w', limitSizeid)

def limitSizename(*args):
    value1 = nameValue.get()
    if len(value1) > 12: nameValue.set(value1[:12])

nameValue = StringVar()
nameValue.trace('w', limitSizename)

def clear_id():
    id_txt.delete(first=0,last = 10)

def clear_name():
    name_txt.delete(first=0,last = 15)

id_txt = tk.Entry(windo, width=13, bg="white", fg="black", font=('times', 22, ' bold '), textvariable=idValue)
id_txt.place(x=280, y=125)

name_l = tk.Label(windo, text="Enter Name", width=13, height=1, fg="white", bg="midnightblue", font=('times', 14, ' bold '))
name_l.place(x=280, y=175)

name_txt = tk.Entry(windo, width=13, bg="white", fg="black", font=('times', 22, ' bold '), textvariable=nameValue)
name_txt.place(x=280, y=202)

clearButton = tk.Button(windo, command = clear_id,text="Clear",fg="white"  ,bg="midnightblue"  ,width=5  ,height=1 ,activebackground = "yellow" ,font=('times', 12, ' bold '))
clearButton.place(x=490, y=127)

clearButton1 = tk.Button(windo,command = clear_name, text="Clear",fg="white"  ,bg="midnightblue"  ,width=5 ,height=1, activebackground = "yellow" ,font=('times', 12, ' bold '))
clearButton1.place(x=490, y=204)

def open_fd():
    subprocess.Popen(r'explorer /select,"TrainingImage"')

cm = tk.Button(windo,command = open_fd, text="Check Face\ud83d\ude00 Images",fg="white"  ,bg="midnightblue"  ,width=18 ,height=1, activebackground = "yellow" ,font=('times', 18, ' bold '))
cm.place(x=280, y=290)

cd = tk.Button(windo, text="Registered Employees",fg="white"  ,bg="midnightblue"  ,width=18 ,height=1, activebackground = "yellow" ,font=('times', 18, ' bold '))
cd.place(x=280, y=350)

my_name = tk.Label(windo, text="©Developed by Kushal Bhavsar", bg="midnightblue", fg="white", width=58,
                   height=1, font=('times', 30, 'italic bold '))
my_name.place(x=0, y=640)

start = tk.Label(windo, text="Employee Attendance using Face\ud83d\ude00 Recognition", bg="midnightblue", fg="white", width=58,
                   height=1, font=('times', 30, 'italic bold '))
start.place(x=0, y=0)

start1 = tk.Label(windo, text="Enter your Face\ud83d\ude00 Data if you are a new user!", bg="yellow", fg="black", width=35,
                   height=1, font=('times', 20, 'bold '))
start1.place(x=0, y=50)

def tick():
    global time1
    time2 = time.strftime('%H:%M:%S')
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    clock.after(200, tick)

time1 = ''
clock = Label(windo, font=('times', 20, 'bold'), bg='white')
clock.place(x=1160, y = 7)
tick()

sg = PhotoImage(file = "./images/cartoon.png")
sg_f = tk.Button(windo, borderwidth=0, image = sg,bg = 'white',command = image_generate )
sg_f.place(x=50, y=480)

ca = tk.Label(windo, text="Generate Faces", bg="midnightblue", fg="white", width=11,
                   height=1, font=('times', 16, 'italic bold '))
ca.place(x=48, y=590)

tm = PhotoImage(file = "./images/train.png")
t_m = tk.Button(windo,borderwidth=0,bg = 'white',image = tm,command = model_training)
t_m.place(x=250, y=480)

tb = tk.Label(windo, text="Train Model", bg="midnightblue", fg="white", width=11,
                   height=1, font=('times', 16, 'italic bold '))
tb.place(x=248, y=587)

windo.mainloop()
from tkinter import filedialog
from tkinter import *
import tkinter as tk
from PIL import ImageTk,Image
import cv2
import numpy as np
import datetime,subprocess
import pyttsx3
import time,csv,os
from pathlib import Path

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
            imageFrame.place(x=665, y=50)

            dn = tk.Label(windo, text='Generating Face\ud83d\ude00 Dataset of: '+ name, width=30, height=1, fg="white", bg="midnightblue",
                           font=('times', 19, ' bold '))
            dn.place(x=670, y=10)

            display = tk.Label(imageFrame)
            display.grid()

            imageFrame1 = tk.Frame(windo)
            imageFrame1.place(x= 50, y=88)

            display1 = tk.Label(imageFrame1, borderwidth = 6,highlightbackground='yellow')
            display1.grid()

            ip = tk.Label(windo, text= name, width=14, height=1, fg="black", bg="yellow",
                          font=('times', 18, ' bold '))
            ip.place(x=50, y=260)
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
                    dn.configure(text = 'Images Captured',bg = 'springgreen',fg = 'black')
                    windo.after(3000,destroy_widget,ic)
                    windo.after(4000, destroy_widget, dn)
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


def destroy_widget(widget):
    widget.destroy()

def breakcam():
    cam.release()

sad_img = ImageTk.PhotoImage(Image.open("./images/cp1.jpg"))
panel4 = Label(windo, image=sad_img)
panel4.pack()
panel4.place(x=20, y=35)

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
cm.place(x=300, y=290)

cd = tk.Button(windo, text="Registered Employees",fg="white"  ,bg="midnightblue"  ,width=18 ,height=1, activebackground = "yellow" ,font=('times', 18, ' bold '))
cd.place(x=300, y=350)

my_name = tk.Label(windo, text="©Developed by Kushal Bhavsar", bg="midnightblue", fg="white", width=58,
                   height=1, font=('times', 30, 'italic bold '))
my_name.place(x=00, y=640)

sg = PhotoImage(file = "./images/cartoon.png")
sg_f = tk.Button(windo, borderwidth=0, image = sg,bg = 'white',command = image_generate )
sg_f.place(x=50, y=480)

ca = tk.Label(windo, text="Generate Faces", bg="midnightblue", fg="white", width=11,
                   height=1, font=('times', 16, 'italic bold '))
ca.place(x=48, y=590)

tm = PhotoImage(file = "./images/train.png")
t_m = tk.Button(windo,borderwidth=0,bg = 'white',image = tm)
t_m.place(x=250, y=480)

tb = tk.Label(windo, text="Train Model", bg="midnightblue", fg="white", width=11,
                   height=1, font=('times', 16, 'italic bold '))
tb.place(x=248, y=587)

windo.mainloop()
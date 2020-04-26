from tkinter.ttk import Progressbar
import tkinter

class Example(tkinter.Frame):
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        value_progress =50
        self.parent.title("Progressbar Thingymawhatsit")
        self.config(bg = '#F0F0F0')
        self.pack(fill = tkinter.BOTH, expand = 1)
                #create canvas
        canvas = tkinter.Canvas(self, relief = tkinter.FLAT, background = "#D2D2D2",
                                            width = 400, height = 5)

        progressbar = Progressbar(canvas, orient=tkinter.HORIZONTAL,
                                  length=400, mode="indeterminate",
                                  variable=value_progress,
                                  )
        # The first 2 create window argvs control where the progress bar is placed
        canvas.create_window(1, 1, anchor=tkinter.NW, window=progressbar)
        canvas.grid()


def main():
    root = tkinter.Tk()
    root.geometry('500x50+10+50')
    app = Example(root)
    app.mainloop()

if __name__ == '__main__':
    main()
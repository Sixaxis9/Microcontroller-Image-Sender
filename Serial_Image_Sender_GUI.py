from tkinter import *
from GUI import *

window = Tk()

window.title("Serial Image Sender")
#iconbitmap(self, default="clienticon.ico")

gui = GUI(window)
gui.UI_init()

window.geometry('640x420')
window.mainloop()
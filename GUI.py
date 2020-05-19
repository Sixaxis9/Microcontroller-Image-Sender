from tkinter import *

from serial_class import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import os

class GUI:
    def __init__(self, window):
        self.i = 0
        self.image_list = []
        self.directory = ""
        self.window = window
        self.Serial = Serial("COM3")


    # Function definition
    def com_clicked(self):
        self.Serial.serial_begin(self.com_port_entry.get())
        if self.Serial.get_serial_status():
            print("Port open!")

    def next_image(self):
        if self.i==0:
            self.directory = self.path_to_folder_entry.get()
            self.image_list = os.listdir(self.directory)
        image = prep_img(self.directory + "/" + self.image_list[self.i])
        self.ax.clear()
        self.ax.imshow(image)
        self.i+=1
        self.canvas.draw()

        self.Serial.serial_send(image)
        received = self.Serial.serial_receive_int(1)
        if received != -1:
            self.predicted_label_2.configure(text=str(received))

    # Frames definitions
    def frame_init(self):
        self.controls_frm = Frame(master=self.window)
        self.inputs_I_frm = Frame(master=self.controls_frm)
        self.inputs_II_frm = Frame(master=self.controls_frm)

        self.metrics_frm = Frame(master=self.window)

        self.mode_frm = Frame(master=self.window)
        self.buttons_frm = Frame(master=self.mode_frm)

    def widgets_init(self):
        self.path_to_folder_lbl = Label(text="Path to folder", master=self.inputs_I_frm)
        self.path_to_folder_entry = Entry(width=30, master=self.inputs_I_frm)
        self.path_to_folder_entry.focus()

        self.path_to_img_ann_lbl = Label(text="Path to image annotations", master=self.inputs_I_frm)
        self.path_to_img_ann_entry = Entry(width=30, master=self.inputs_I_frm)

        self.path_to_ground_truth_lbl = Label(text="Path to ground truth", master=self.inputs_I_frm)
        self.path_to_ground_truth_entry = Entry(width=30, master=self.inputs_I_frm)

        self.predicted_label_1 = Label(text="Predicted label:", master=self.inputs_II_frm)
        self.predicted_label_2 = Label(text="", master=self.inputs_II_frm)

        self.x_size_lbl = Label(text="X size", master=self.inputs_II_frm)
        self.y_size_lbl = Label(text="Y size", master=self.inputs_II_frm)
        self.com_port_lbl = Label(text="Select COM", master=self.inputs_II_frm)

        self.x_size_entry = Entry(width=10, master=self.inputs_II_frm)
        self.y_size_entry = Entry(width=10, master=self.inputs_II_frm)
        self.com_port_entry = Entry(width=10, master=self.inputs_II_frm)
        self.connect_btn = Button(text="Connect", command=self.com_clicked, master=self.inputs_II_frm)

        self.correct_counter_lbl = Label(text="Predicted label:", master=self.metrics_frm)
        self.correct_percentage_lbl = Label(text="oecentage", master=self.metrics_frm)
        self.sent_counter_lbl = Label(text="all count", master=self.metrics_frm)
        self.accuracy_lbl = Label(text="acc", master=self.metrics_frm)

        self.next_image_btn = Button(text="Next Image", command=self.next_image, master=self.buttons_frm)
        self.start_burst_btn = Button(text="Start burst", command=self.com_clicked, master=self.buttons_frm)

        self.self_bragging_lbl = Label(text="Image sender by Marco Giordano", master=self.mode_frm)
    
    def image_show_init(self):
        fig = Figure(figsize=(3, 3), dpi=100)
        self.ax = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self.window)  # A tk.DrawingArea.
        self.canvas.draw()


    # Grid positioning

    # Inputs
    def widget_positining(self):
        self.path_to_folder_lbl.grid(row=0, column=0, padx=5, pady=5)
        self.path_to_folder_entry.grid(row=1, column=0, padx=0, pady=5)

        self.path_to_img_ann_lbl.grid(row=2, column=0, padx=5, pady=5)
        self.path_to_img_ann_entry.grid(row=3, column=0, padx=0, pady=5)

        self.path_to_ground_truth_lbl.grid(row=4, column=0, padx=5, pady=5)
        self.path_to_ground_truth_entry.grid(row=5, column=0, padx=0, pady=5)

        self.predicted_label_1.grid(row=0, column=0, padx=5, pady=20)
        self.predicted_label_2.grid(row=0, column=1, padx=5, pady=20)

        self.x_size_lbl.grid(row=1, column=0, padx=5, pady=5)
        self.y_size_lbl.grid(row=1, column=1, padx=5, pady=5)
        self.com_port_lbl.grid(row=1, column=2, padx=5, pady=5)

        self.x_size_entry.grid(row=2, column=0, padx=5, pady=5)
        self.y_size_entry.grid(row=2, column=1, padx=5, pady=5)
        self.com_port_entry.grid(row=2, column=2, padx=5, pady=5)
        self.connect_btn.grid(row=2, column=3, padx=5, pady=5)

        self.correct_counter_lbl.grid(row=0, column=0, padx=5, pady=10)
        self.correct_percentage_lbl.grid(row=0, column=1, padx=5, pady=10)
        self.sent_counter_lbl.grid(row=1, column=0, padx=5, pady=10)
        self.accuracy_lbl.grid(row=1, column=1, padx=5, pady=10)


        self.canvas.get_tk_widget().grid(row=0, column=0)

        self.next_image_btn.grid(row=0, column=0, padx=20, pady=20)
        self.start_burst_btn.grid(row=0, column=1, padx=20, pady=20)

        self.self_bragging_lbl.grid(row=1, column=0)


    # Frames
    def frame_positioning(self):
        self.controls_frm.grid(row=0, column=1)
        self.inputs_I_frm.grid(row=0, column=0)
        self.inputs_II_frm.grid(row=1, column=0)

        self.metrics_frm.grid(row=1, column=1)

        self.mode_frm.grid(row=1, column=0)
        self.buttons_frm.grid(row=0, column=0)

    def UI_init(self):
        self.frame_init()
        self.widgets_init()
        self.image_show_init()
        self.widget_positining()
        self.frame_positioning()
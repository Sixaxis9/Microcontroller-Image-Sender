from tkinter import *

from serial_class import *

import numpy as np

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
        self.all_inference=0
        self.correct_inference=0
        self.berserk_mode = 0

    # Function definition
    def com_clicked(self):
        self.Serial.serial_begin(self.com_port_entry.get())
        if self.Serial.get_serial_status():
            self.window.after(100, self.read_from_serial)
            self.connect_btn.configure(text="Connected", bg='green')


    def next_image(self):
        if self.i==0:
            self.directory = self.path_to_folder_entry.get()
            self.image_list = os.listdir(self.directory)
            self.next_image_btn.configure(text="Next image")
            self.img_ann = np.empty(0)
            self.labels = np.empty(0)
            self.gnd_trh = np.empty(0)

            if os.path.exists(self.path_to_img_ann_entry.get()):
                self.img_ann = np.loadtxt(self.path_to_img_ann_entry.get(), delimiter=',')
            if os.path.exists(self.path_to_ground_truth_entry.get()):
                self.labels = self.gnd_trh = np.loadtxt(self.path_to_ground_truth_entry.get(), max_rows=1, delimiter=',', dtype='str')
                self.gnd_trh = np.loadtxt(self.path_to_ground_truth_entry.get(), skiprows=1)

        if self.img_ann.shape[-1] != 0:
            self.image = prep_img(self.directory + "/" + self.image_list[self.i], int(self.x_size_entry.get()),
                        int(self.y_size_entry.get()), self.img_ann[self.i])
        else:
            self.image = prep_img(self.directory + "/" + self.image_list[self.i], int(self.x_size_entry.get()),
                        int(self.y_size_entry.get()))

        self.ax.clear()
        self.ax.imshow(self.image)
        self.i+=1
        self.canvas.draw()

        self.predicted_label_2.configure(text="---")
        self.ground_truth_2.configure(text="---")
        self.predicted_label_1.configure(bg="SystemButtonFace")
        self.predicted_label_2.configure(bg="SystemButtonFace")
        self.ground_truth_1.configure(bg="SystemButtonFace")
        self.ground_truth_2.configure(bg="SystemButtonFace")
        
        self.Serial.serial_send(self.image)

    def berserk_button(self):
        if self.berserk_mode == 0:
            self.berserk_mode = 1
            self.next_image()
            self.start_burst_btn.configure(bg="Purple")
        else:
            self.berserk_mode = 0
            self.start_burst_btn.configure(bg="SystemButtonFace")
        

    def read_from_serial(self):
        infered_class = self.Serial.serial_receive_int()
        accuracy = self.Serial.serial_receive_float()
        cycles = self.Serial.serial_receive_32bit_uint()
        if infered_class != -1:
            self.predicted_label_2.configure(text=str(infered_class))
            if self.labels.shape[-1] != 0:
                self.predicted_label_2.configure(text=self.predicted_label_2.cget("text") + 
                                            ", " + self.labels[int(infered_class)])
                if self.gnd_trh.shape[-1] != 0:
                    self.ground_truth_2.configure(text=str(int(self.gnd_trh[self.i-1])) + ", " 
                        + self.labels[int(self.gnd_trh[self.i-1])])
                    if int(infered_class) == int(self.gnd_trh[self.i-1]):
                        self.predicted_label_1.configure(bg='green')
                        self.predicted_label_2.configure(bg='green')
                        self.ground_truth_1.configure(bg='green')
                        self.ground_truth_2.configure(bg='green')
                        self.correct_inference += 1
                    else:
                        self.predicted_label_1.configure(bg='red')
                        self.predicted_label_2.configure(bg='red')
                        self.ground_truth_1.configure(bg='red')
                        self.ground_truth_2.configure(bg='red')
        
            self.all_inference += 1
            self.correct_counter_lbl_display.configure(text=str(self.correct_inference))
            self.correct_percentage_lbl_display.configure(text='{:.2f}'.format(self.correct_inference/self.all_inference*100))
            self.sent_counter_lbl_display.configure(text=int(self.all_inference))
            if self.berserk_mode:
                self.next_image()
        
        if accuracy != -1:
            self.accuracy_lbl_display.configure(text='{:.2f}'.format(accuracy))

        if cycles != -1:
            self.cycle_counter_lbl_display.configure(text=str(cycles))
            self.time_for_inference_lbl_display.configure(text='{:.2f} ms'.format(cycles/80000))

        self.window.after(100, self.read_from_serial)


    # Frames definitions
    def frame_init(self):
        self.controls_frm = Frame(master=self.window)
        self.inputs_I_frm = Frame(master=self.controls_frm)
        self.inputs_II_frm = Frame(master=self.controls_frm)
        self.inputs_III_frm = Frame(master=self.controls_frm)

        self.metrics_frm = Frame(master=self.window)

        self.mode_frm = Frame(master=self.window)
        self.buttons_frm = Frame(master=self.mode_frm)

    def widgets_init(self):
        self.path_to_folder_lbl = Label(text="Path to folder", master=self.inputs_I_frm)
        self.path_to_folder_entry = Entry(width=30, master=self.inputs_I_frm)
        self.path_to_folder_entry.insert(END, "./test_images")

        self.path_to_img_ann_lbl = Label(text="Path to image annotations", master=self.inputs_I_frm)
        self.path_to_img_ann_entry = Entry(width=30, master=self.inputs_I_frm)
        self.path_to_img_ann_entry.insert(END, "./image_annotation.csv")

        self.path_to_ground_truth_lbl = Label(text="Path to ground truth", master=self.inputs_I_frm)
        self.path_to_ground_truth_entry = Entry(width=30, master=self.inputs_I_frm)
        self.path_to_ground_truth_entry.insert(END, "./ground_truth.csv")

        self.predicted_label_1 = Label(text="Predicted label:", master=self.inputs_II_frm)
        self.predicted_label_2 = Message(text="----------", master=self.inputs_II_frm, width=200)
        self.ground_truth_1 = Label(text="Ground truth:", master=self.inputs_II_frm)
        self.ground_truth_2 = Message(text="----------", master=self.inputs_II_frm, width=200)

        self.x_size_lbl = Label(text="X size", master=self.inputs_III_frm)
        self.y_size_lbl = Label(text="Y size", master=self.inputs_III_frm)
        self.com_port_lbl = Label(text="Select COM", master=self.inputs_III_frm)

        self.x_size_entry = Entry(width=10, master=self.inputs_III_frm)
        self.x_size_entry.insert(END, '32')
        self.y_size_entry = Entry(width=10, master=self.inputs_III_frm)
        self.y_size_entry.insert(END, '32')
        self.com_port_entry = Entry(width=10, master=self.inputs_III_frm)
        #self.com_port_entry.focus()
        self.com_port_entry.insert(END, 'COM3')
        self.connect_btn = Button(text="Connect", command=self.com_clicked, master=self.inputs_III_frm)

        self.correct_counter_lbl = Label(text="Correct prediction:", master=self.metrics_frm)
        self.correct_percentage_lbl = Label(text="Correct percentage", master=self.metrics_frm)
        self.sent_counter_lbl = Label(text="All predictions", master=self.metrics_frm)
        self.accuracy_lbl = Label(text="Last accuracy", master=self.metrics_frm)
        self.cycle_counter_lbl = Label(text="Number of cycles", master=self.metrics_frm)
        self.time_for_inference_lbl = Label(text="Time for inference", master=self.metrics_frm)
        self.correct_counter_lbl_display = Label(text="---", master=self.metrics_frm)
        self.correct_percentage_lbl_display = Label(text="---", master=self.metrics_frm)
        self.sent_counter_lbl_display = Label(text="---", master=self.metrics_frm)
        self.accuracy_lbl_display = Label(text="---", master=self.metrics_frm)
        self.cycle_counter_lbl_display = Label(text="---", master=self.metrics_frm)
        self.time_for_inference_lbl_display = Label(text="---", master=self.metrics_frm)

        self.next_image_btn = Button(text="Send image", command=self.next_image, master=self.buttons_frm)
        self.start_burst_btn = Button(text="Berserk mode", command=self.berserk_button, master=self.buttons_frm)

        self.self_bragging_lbl = Label(text="Image sender by Marco Giordano", master=self.mode_frm)
    
    def image_show_init(self):
        fig = Figure(figsize=(3, 3), dpi=100)
        self.ax = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self.window)
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

        self.predicted_label_1.grid(row=0, column=0, padx=5, pady=10)
        self.predicted_label_2.grid(row=0, column=1, padx=5, pady=10)
        self.ground_truth_1.grid(row=1, column=0, padx=5, pady=10)
        self.ground_truth_2.grid(row=1, column=1, padx=5, pady=10)

        self.x_size_lbl.grid(row=0, column=0, padx=5, pady=5)
        self.y_size_lbl.grid(row=0, column=1, padx=5, pady=5)
        self.com_port_lbl.grid(row=0, column=2, padx=5, pady=5)

        self.x_size_entry.grid(row=1, column=0, padx=5, pady=5)
        self.y_size_entry.grid(row=1, column=1, padx=5, pady=5)
        self.com_port_entry.grid(row=1, column=2, padx=5, pady=5)
        self.connect_btn.grid(row=1, column=3, padx=5, pady=5)

        self.correct_counter_lbl.grid(row=0, column=0, padx=5, pady=10)
        self.correct_percentage_lbl.grid(row=0, column=2, padx=5, pady=10)
        self.sent_counter_lbl.grid(row=1, column=0, padx=5, pady=10)
        self.accuracy_lbl.grid(row=1, column=2, padx=5, pady=10)
        self.cycle_counter_lbl.grid(row=2, column=0, padx=5, pady=10)
        self.time_for_inference_lbl.grid(row=2, column=2, padx=5, pady=10)
        self.correct_counter_lbl_display.grid(row=0, column=1, padx=5, pady=10)
        self.correct_percentage_lbl_display.grid(row=0, column=3, padx=5, pady=10)
        self.sent_counter_lbl_display.grid(row=1, column=1, padx=5, pady=10)
        self.accuracy_lbl_display.grid(row=1, column=3, padx=5, pady=10)
        self.cycle_counter_lbl_display.grid(row=2, column=1, padx=5, pady=10)
        self.time_for_inference_lbl_display.grid(row=2, column=3, padx=5, pady=10)

        self.canvas.get_tk_widget().grid(row=0, column=0)

        self.next_image_btn.grid(row=0, column=0, padx=20, pady=5)
        self.start_burst_btn.grid(row=0, column=1, padx=20, pady=5)

        self.self_bragging_lbl.grid(row=1, column=0, padx=0, pady=10)


    # Frames
    def frame_positioning(self):
        self.controls_frm.grid(row=0, column=1)
        self.inputs_I_frm.grid(row=0, column=0)
        self.inputs_II_frm.grid(row=1, column=0)
        self.inputs_III_frm.grid(row=2, column=0)

        self.metrics_frm.grid(row=1, column=1)

        self.mode_frm.grid(row=1, column=0)
        self.buttons_frm.grid(row=0, column=0)

    def UI_init(self):
        self.frame_init()
        self.widgets_init()
        self.image_show_init()
        self.widget_positining()
        self.frame_positioning()
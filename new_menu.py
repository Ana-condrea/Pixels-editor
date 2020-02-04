import random
import tkinter as tk
from tkinter import *
from tkinter import filedialog, Scale, messagebox

import cv2
import numpy as np
import os
import soundfile as sf
import re
from PIL import Image, ImageTk

from first_alg import load, unload_show
from hide_image_in_audio import load_image_in_audio, extract_image_px, extract_list, compute_image
from hide_image_in_video import hide_image_in_frame, unload_image_from_video
from hide_text_in_audio import load_text_in_audio, unload_text_from_audio
from hide_text_in_video import change_frame_in_video, load_text_in_video, unload_text_from_video
from second_alg_invisible import load_text_invisible, unload_text_invisible
from second_alg_random_poz import load_text_random, unload_text_random
from third_alg import final_load_audio, unload_audio, make_new_image
from watermark_img_1 import add_watermark_img, remove_watermark_img
from watermark_text_1 import add_watermark_text, remove_watermark_text, create_txt_image
from watermark_video_1 import add_watermark_image_video, add_watermark_text_video, remove_watermark_image_video, \
    remove_watermark_text_video

title_font = ('Helvetica', 20, 'bold')
title_font1 = ('Helvetica', 15, 'bold')
font = ('Arial', 14)
bite = 4
path1 = ""
path2 = ""
text = ""
color = ""
number = 0
alpha = 1
dictionary_positions = dict()
size_img = list()
poz_x, poz_y = 0, 0


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Steganography")
        self.geometry("430x650")

        page = tk.Frame(self)
        page.pack(side="top", fill="both", expand=True)
        page.grid_rowconfigure(0, weight=1)
        page.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for P in (MainPage, PageOne, PageTwoV1, PageTwoV2, MainPageThree, PageThree, PageThreeV1,
                  PageThreeV2, MainPageFour, PageFourV1, PageFourV2, PageFiveV1, PageFiveV2,
                  PageFiveV3, PageFiveV4, MainPageFive, MainPageTwo):
            pg = P(page, self)
            self.pages[P] = pg
            pg.grid(row=0, column=0, sticky="nsew")

        self.show_page(MainPage)

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        image = Image.open("c3.jpg")
        photo = ImageTk.PhotoImage(image)
        img = tk.Label(self, image=photo)
        img.image = photo
        img.place(x=0, y=0)

        label = tk.Label(self, text='Menu', font=title_font, fg='#d4cc79', bg="#354966")
        label.pack(pady=60, padx=30, side="top", fill="both")

        button1 = tk.Button(self, text='Hide image', width=15,
                            command=lambda: controller.show_page(PageOne), bg="#f1f5d3", font=font, cursor="hand2")
        button1.pack(pady=10, padx=30, side="top", fill="both")

        button2 = tk.Button(self, text='Hide text', width=15,
                            command=lambda: controller.show_page(MainPageTwo), bg="#f1f5d3", font=font, cursor="hand2")
        button2.pack(pady=10, padx=30, side="top", fill="both")

        button3 = tk.Button(self, text='Hide audio', width=15, command=lambda: controller.show_page(MainPageThree),
                            bg="#f1f5d3", font=font, cursor="hand2")
        button3.pack(pady=10, padx=30, side="top", fill="both")

        button4 = tk.Button(self, text='Hide video', width=15,
                            command=lambda: controller.show_page(MainPageFour), bg="#f1f5d3", font=font, cursor="hand2")
        button4.pack(pady=10, padx=30, side="top", fill="both")

        button5 = tk.Button(self, text='Watermark', width=15,
                            command=lambda: controller.show_page(MainPageFive), bg="#f1f5d3", font=font, cursor="hand2")
        button5.pack(pady=10, padx=30, side="top", fill="both")


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Hide image in image', font=title_font)
        label.pack(pady=30, padx=20, side="top", fill='both')

        frame_path_one = tk.Frame(self)
        frame_path_one.pack(fill=X)

        label_path_one = tk.Label(frame_path_one, text="Path Cover Image", width=15)
        label_path_one.pack(side=LEFT, padx=5, pady=5)

        self.path_one = Entry(frame_path_one)
        self.path_one.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_one, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=5)
        button_browse.pack(pady=10, padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse_one = tk.Frame(self)
        frame_browse_one.pack(fill=X)

        label_or_one = tk.Label(frame_browse_one, text="or", width=10)
        label_or_one.pack(side=TOP, padx=5)

        button_browse_one = tk.Button(frame_browse_one, text="Browse A File", command=self.file_dialog,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_one.pack(pady=5, padx=100, side="left", expand=True, fill=X)

        frame_path_two = tk.Frame(self)
        frame_path_two.pack(fill=X)

        label_path_two = tk.Label(frame_path_two, text="Path Image to Hide", width=15)
        label_path_two.pack(side=LEFT, padx=5, pady=5)

        self.path_two = Entry(frame_path_two)
        self.path_two.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_two, text="Set Path", command=self.get_path_two, font=('Arial', 10),
                                  cursor="hand2", width=5)
        button_browse.pack(pady=10, padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse_two = tk.Frame(self)
        frame_browse_two.pack(fill=X)

        label_or_two = tk.Label(frame_browse_two, text="or", width=10)
        label_or_two.pack(side=TOP, padx=5)

        button_browse_two = tk.Button(frame_browse_two, text="Browse A File", command=self.file_dialog_two,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_two.pack(pady=5, padx=100, side="left", expand=True, fill=X)

        frame_scale = Frame(self)
        frame_scale.pack(fill=X, pady=10)
        label_scale = tk.Label(frame_scale, text="Number of byte", width=15)
        label_scale.pack(side=LEFT, pady=10, padx=5)

        scale = Scale(frame_scale, from_=1, to=7, orient=HORIZONTAL, tickinterval=1)
        scale.pack(side=LEFT, padx=5, expand=True, fill=X)

        def set_values():
            global bite
            bite = scale.get()

        button = Button(frame_scale, text="Set value", command=set_values, font=('Arial', 10), cursor="hand2", width=10)
        button.pack(side=LEFT, padx=20)

        frame_space = Frame(self)
        frame_space.pack(fill=X, pady=25)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            if path1 == "" or path2 == "" or (bite < 1 or bite > 7):
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Path of the cover image does not exists!')
                    self.path_one.delete(0, 'end')
                elif os.path.exists(path2) is False:
                    messagebox.showinfo("Error", 'Path of the image to hide does not exists!')
                    self.path_two.delete(0, 'end')
                elif os.path.exists(path1) and os.path.exists(path2):
                    img = cv2.imread(path1, cv2.IMREAD_COLOR)
                    image2 = cv2.imread(path2, cv2.IMREAD_COLOR)
                    height, width = img.shape[:2]
                    height2, width2 = image2.shape[:2]
                    if height2 > height or width2 > width:
                        self.path_one.delete(0, 'end')
                        self.path_two.delete(0, 'end')
                        messagebox.showinfo("Message", 'Image 2 should not be larger than Image 1!')
                    else:
                        load(img, image2, bite)
                        self.path_one.delete(0, 'end')

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path1 == "" or path2 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Path of the modified image does not exists!')
                    self.path_one.delete(0, 'end')
                elif os.path.exists(path1) and os.path.exists(path2):
                    path_image_load = path1
                    image2 = cv2.imread(path2, cv2.IMREAD_COLOR)
                    size = image2.shape[:2]
                    unload_show(path_image_load, size, bite, 1)
                    self.path_one.delete(0, 'end')
                    self.path_two.delete(0, 'end')

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back to Home', width=15, command=lambda: controller.
                                show_page(MainPage), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path_one.get().replace('\\', '\\\\')

    def get_path_two(self):
        global path2
        path2 = self.path_two.get().replace('\\', '\\\\')

    filename = ""
    filename1 = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                   filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path_one.delete(0, END)
        self.path_one.insert(0, self.filename)
        self.get_path()

    def file_dialog_two(self):
        self.filename1 = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                    filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path_two.delete(0, END)
        self.path_two.insert(0, self.filename1)
        self.get_path_two()


class MainPageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        image = Image.open("c3.jpg")
        photo = ImageTk.PhotoImage(image)
        img = tk.Label(self, image=photo)
        img.image = photo
        img.place(x=0, y=0)

        label = tk.Label(self, text='Menu', font=title_font, fg='#d4cc79', bg="#354966")
        label.pack(pady=40, padx=30, side="top", fill="both")

        button1 = tk.Button(self, text='Hide text invisible', width=15,
                            command=lambda: controller.show_page(PageTwoV1), bg="#f1f5d3", font=font, cursor="hand2")
        button1.pack(pady=10, padx=30, side="top", fill="both")

        button2 = tk.Button(self, text='Hide text visible', width=15,
                            command=lambda: controller.show_page(PageTwoV2), bg="#f1f5d3", font=font, cursor="hand2")
        button2.pack(pady=10, padx=30, side="top", fill="both")

        button_back = tk.Button(self, text='Back to Home', width=15, command=lambda: controller.
                                show_page(MainPage), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, padx=60, expand=True, fill=X)


class PageTwoV1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Hide text invisible', font=title_font)
        label.pack(pady=30, padx=20, side="top", fill='both')

        frame_path = tk.Frame(self)
        frame_path.pack(fill=X)

        label_path = tk.Label(frame_path, text="File Path", width=7)
        label_path.pack(side=LEFT, padx=5, pady=5)

        self.path = Entry(frame_path)
        self.path.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=3)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse = tk.Frame(self)
        frame_browse.pack(fill=X)

        label_or = tk.Label(frame_browse, text="or", width=10)
        label_or.pack(side=TOP, padx=5)

        button_browse = tk.Button(frame_browse, text="Browse A File", command=self.file_dialog, font=('Arial', 10),
                                  cursor="hand2", width=5)
        button_browse.pack(pady=10, padx=100, side="left", expand=True, fill=X)

        frame_text = tk.Frame(self)
        frame_text.pack(expand=True)

        label_txt = tk.Label(frame_text, text="Text", width=7)
        label_txt.pack(side=LEFT, anchor=N, padx=3)
        button_browse = tk.Button(frame_text, text="Set Text", command=self.get_text, font=('Arial', 10),
                                  cursor="hand2", width=14)
        button_browse.pack(side=BOTTOM, padx=10, pady=10, anchor=E)

        self.txt = tk.Text(frame_text)
        self.txt.configure(height=10)
        self.txt.pack(side=LEFT, padx=10)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            if path1 == "" or text == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Path image does not exists!')
                    self.path.delete(0, 'end')
                else:
                    img = cv2.imread(path1, cv2.IMREAD_COLOR)
                    load_text_invisible(img, text)
                    self.path.delete(0, 'end')
                    self.txt.delete('1.0', 'end')

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path1 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Path of the modified image does not exists!')
                    self.path.delete(0, 'end')
                else:
                    rez = unload_text_invisible(path1)
                    self.path.delete(0, 'end')
                    messagebox.showinfo("Message", rez)

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageTwo), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path.get().replace('\\', '\\\\')

    def get_text(self):
        global text
        text = self.txt.get("1.0", "end-1c")
        if len(text) > 255:
            self.txt.delete('1.0', 'end')
            messagebox.showinfo("Error", "Length of the text should be lower that 256 character!")

    filename = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                   filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path.delete(0, END)
        self.path.insert(0, self.filename)
        self.get_path()


class PageTwoV2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Hide text visible', font=title_font)
        label.pack(pady=30, padx=20, side="top", fill='both')

        frame_path = tk.Frame(self)
        frame_path.pack(fill=X)

        label_path = tk.Label(frame_path, text="File Path", width=10)
        label_path.pack(side=LEFT, padx=5, pady=5)

        self.path = Entry(frame_path)
        self.path.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=3)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse = tk.Frame(self)
        frame_browse.pack(fill=X)

        label_or = tk.Label(frame_browse, text="or", width=10)
        label_or.pack(side=TOP, padx=5)

        button_browse = tk.Button(frame_browse, text="Browse A File", command=self.file_dialog, font=('Arial', 10),
                                  cursor="hand2", width=5)
        button_browse.pack(pady=10, padx=100, side="left", expand=True, fill=X)

        frame_text = tk.Frame(self)
        frame_text.pack(expand=True)

        label_txt = tk.Label(frame_text, text="Text", width=10)
        label_txt.pack(side=LEFT, anchor=N, padx=3)
        button_browse = tk.Button(frame_text, text="Set Text", command=self.get_text, font=('Arial', 10),
                                  cursor="hand2", width=10)
        button_browse.pack(side=BOTTOM, padx=10, pady=10, anchor=E)

        self.txt = tk.Text(frame_text)
        self.txt.configure(height=10)
        self.txt.pack(side=LEFT, padx=10)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load_random():
            if path1 == "" or text == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Path image does not exists!')
                    self.path.delete(0, 'end')
                else:
                    img = cv2.imread(path1, cv2.IMREAD_COLOR)
                    load_text_random(img, text)
                    self.path.delete(0, 'end')
                    self.txt.delete('1.0', 'end')

        button_load = tk.Button(frame_buttons, text='Load', width=10,
                                command=final_load_random, bg="#f1f5d3", font=font, cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload_random():
            if path1 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Path of the modified image does not exists!')
                    self.path.delete(0, 'end')
                else:
                    rez = unload_text_random(path1)
                    self.path.delete(0, 'end')
                    messagebox.showinfo("Message", rez)

        button_unload = tk.Button(frame_buttons, text='Unload', width=10,
                                  command=final_unload_random, bg="#f1f5d3", font=font, cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageTwo), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path.get().replace('\\', '\\\\')

    def get_text(self):
        global text
        text = self.txt.get("1.0", "end-1c")
        if len(text) > 255:
            self.txt.delete('1.0', 'end')
            messagebox.showinfo("Error", "Length of the text should be lower that 256 character!")

    filename = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                   filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path.delete(0, END)
        self.path.insert(0, self.filename)
        self.get_path()


class MainPageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        image = Image.open("c3.jpg")
        photo = ImageTk.PhotoImage(image)
        img = tk.Label(self, image=photo)
        img.image = photo
        img.place(x=0, y=0)

        label = tk.Label(self, text='Menu', font=title_font, fg='#d4cc79', bg="#354966")
        label.pack(pady=40, padx=30, side="top", fill="both")

        button1 = tk.Button(self, text='Hide audio in image', width=15,
                            command=lambda: controller.show_page(PageThree), bg="#f1f5d3", font=font, cursor="hand2")
        button1.pack(pady=10, padx=30, side="top", fill="both")

        button2 = tk.Button(self, text='Hide image in audio', width=15,
                            command=lambda: controller.show_page(PageThreeV1), bg="#f1f5d3", font=font, cursor="hand2")
        button2.pack(pady=10, padx=30, side="top", fill="both")

        button2 = tk.Button(self, text='Hide text in audio', width=15,
                            command=lambda: controller.show_page(PageThreeV2), bg="#f1f5d3", font=font, cursor="hand2")
        button2.pack(pady=10, padx=30, side="top", fill="both")

        button_back = tk.Button(self, text='Back to Home', width=15, command=lambda: controller.
                                show_page(MainPage), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, padx=60, expand=True, fill=X)


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Hide audio in image', font=title_font)
        label.pack(pady=30, padx=20, side="top", fill='both')

        frame_path_one = tk.Frame(self)
        frame_path_one.pack(fill=X)

        label_path_one = tk.Label(frame_path_one, text="Path Audio", width=13)
        label_path_one.pack(side=LEFT, padx=5, pady=5)

        self.path_one = Entry(frame_path_one)
        self.path_one.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_one, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=7)
        button_browse.pack(pady=10, padx=20, side=RIGHT, expand=True, fill=X)

        frame_browse_one = tk.Frame(self)
        frame_browse_one.pack(fill=X)

        label_or_one = tk.Label(frame_browse_one, text="or", width=10)
        label_or_one.pack(side=TOP, padx=5)

        button_browse_one = tk.Button(frame_browse_one, text="Browse A File", command=self.file_dialog,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_one.pack(pady=5, padx=100, side="left", expand=True, fill=X)

        frame_radio = tk.Frame(self)
        frame_radio.pack(fill=X)

        v = tk.IntVar()

        tk.Label(frame_radio, text="""Choose time length of the audio:""", pady=20, padx=10).pack(anchor=tk.W)
        tk.Radiobutton(frame_radio, text="5 seconds", padx=20, variable=v, value=1).pack(anchor=tk.W, padx=50)
        tk.Radiobutton(frame_radio, text="30 seconds", padx=20, variable=v, value=2).pack(anchor=tk.W, padx=50)

        frame_scale = Frame(self)
        frame_scale.pack(fill=X, pady=10)
        label_scale = tk.Label(frame_scale, text="Number of byte", width=13)
        label_scale.pack(side=LEFT, pady=10, padx=5)

        scale = Scale(frame_scale, from_=1, to=14, orient=HORIZONTAL, tickinterval=1)
        scale.pack(side=LEFT, padx=5, expand=True, fill=X)

        def set_values():
            global bite
            bite = scale.get()

        button = Button(frame_scale, text="Set value", command=set_values, font=('Arial', 10), cursor="hand2", width=7)
        button.pack(side=LEFT, padx=20)

        frame_space = Frame(self)
        frame_space.pack(fill=X, pady=25)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            if path1 == "" or v.get() not in [1, 2] or (bite < 1 or bite > 14):
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Audio path does not exists!')
                    self.path_one.delete(0, 'end')
                else:
                    final_load_audio(bite, path1, v.get())
                    self.path_one.delete(0, 'end')

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path1 == "" or v.get() not in [1, 2] or (bite < 1 or bite > 14):
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Audio path does not exists!')
                    self.path_one.delete(0, 'end')
                else:
                    returned_audio_list = unload_audio(bite, path1, v.get())
                    extract_audio = np.int16(returned_audio_list/np.max(np.abs(returned_audio_list)) * 32767)
                    sf.write('returned_audio.wav', extract_audio, 44100)
                    self.path_one.delete(0, 'end')

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageThree), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path_one.get().replace('\\', '\\\\')

    filename = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An Audio",
                                                   filetype=(("wav files", "*.wav"), ("mp3 files", "*.mp3")))
        self.path_one.delete(0, END)
        self.path_one.insert(0, self.filename)
        self.get_path()


class PageThreeV1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Hide image in audio', font=title_font)
        label.pack(pady=30, padx=20, side="top", fill='both')

        frame_space = Frame(self)
        frame_space.pack(fill=X, pady=20)

        frame_path_one = tk.Frame(self)
        frame_path_one.pack(fill=X)

        label_path_one = tk.Label(frame_path_one, text="Path Audio", width=13)
        label_path_one.pack(side=LEFT, padx=5, pady=5)

        self.path_one = Entry(frame_path_one)
        self.path_one.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_one, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=7)
        button_browse.pack(pady=10, padx=20, side=RIGHT, expand=True, fill=X)

        frame_browse_one = tk.Frame(self)
        frame_browse_one.pack(fill=X)

        label_or_one = tk.Label(frame_browse_one, text="or", width=10)
        label_or_one.pack(side=TOP, padx=5)

        button_browse_one = tk.Button(frame_browse_one, text="Browse A File", command=self.file_dialog,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_one.pack(pady=5, padx=100, side="left", expand=True, fill=X)

        frame_path_two = tk.Frame(self)
        frame_path_two.pack(fill=X)

        label_path_two = tk.Label(frame_path_two, text="Path Image", width=13)
        label_path_two.pack(side=LEFT, padx=5, pady=5)

        self.path_two = Entry(frame_path_two)
        self.path_two.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse_two = tk.Button(frame_path_two, text="Set Path", command=self.get_path_two,
                                      font=('Arial', 10), cursor="hand2", width=7)
        button_browse_two.pack(pady=10, padx=20, side=RIGHT, expand=True, fill=X)

        frame_browse_two = tk.Frame(self)
        frame_browse_two.pack(fill=X)

        label_or_two = tk.Label(frame_browse_two, text="or", width=10)
        label_or_two.pack(side=TOP, padx=5)

        button_browse_two = tk.Button(frame_browse_two, text="Browse A File", command=self.file_dialog_image,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_two.pack(pady=5, padx=100, side="left", expand=True, fill=X)

        frame_space_1 = Frame(self)
        frame_space_1.pack(fill=X, pady=70)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load_image_audio():
            if path1 == "" or path2 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Audio path does not exists!')
                    self.path_one.delete(0, 'end')
                elif os.path.exists(path2) is False:
                    messagebox.showinfo("Error", 'Image path does not exists!')
                    self.path_two.delete(0, 'end')
                elif os.path.exists(path1) and os.path.exists(path2):
                    global dictionary_positions
                    global size_img
                    image_audio = make_new_image(path1)
                    img_to_hide = cv2.imread(path2, cv2.IMREAD_COLOR)
                    size_img = img_to_hide.shape[:3]
                    self.path_one.delete(0, 'end')
                    self.path_two.delete(0, 'end')

                    messagebox.showinfo("Info", "This operation takes time.")
                    img_audio, pozitii_img = load_image_in_audio(image_audio, img_to_hide)
                    cv2.imwrite("image_in_audio.png", image_audio)
                    dictionary_positions = pozitii_img
                    lista_px = extract_list(img_audio)
                    scaled = np.int16(lista_px / np.max(np.abs(lista_px)) * 32767)
                    sf.write('image_in_audio.wav', scaled, 44100)

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load_image_audio,
                                bg="#f1f5d3", font=font, cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path2 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path2) is False:
                    messagebox.showinfo("Error", 'Image path does not exists!')
                    self.path_two.delete(0, 'end')
                else:
                    img_audio = cv2.imread(path2, cv2.IMREAD_COLOR)
                    list_from_audio = extract_image_px(img_audio, dictionary_positions)
                    compute_image(list_from_audio, size_img)
                    self.path_one.delete(0, 'end')

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageThree), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path_one.get().replace('\\', '\\\\')

    def get_path_two(self):
        global path2
        path2 = self.path_two.get().replace('\\', '\\\\')

    filename = ""
    filename1 = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An audio",
                                                   filetype=(("wav files", "*.wav"), ("mp3 files", "*.mp3")))
        self.path_one.delete(0, END)
        self.path_one.insert(0, self.filename)
        self.get_path()

    def file_dialog_image(self):
        self.filename1 = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                    filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path_two.delete(0, END)
        self.path_two.insert(0, self.filename1)
        self.get_path_two()


class PageThreeV2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Hide text in audio', font=title_font)
        label.pack(pady=30, padx=20, side="top", fill='both')

        frame_path_one = tk.Frame(self)
        frame_path_one.pack(fill=X)

        label_path_one = tk.Label(frame_path_one, text="Path Audio", width=13)
        label_path_one.pack(side=LEFT, padx=5, pady=5)

        self.path_one = Entry(frame_path_one)
        self.path_one.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_one, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=7)
        button_browse.pack(pady=10, padx=20, side=RIGHT, expand=True, fill=X)

        frame_browse_one = tk.Frame(self)
        frame_browse_one.pack(fill=X)

        label_or_one = tk.Label(frame_browse_one, text="or", width=10)
        label_or_one.pack(side=TOP, padx=5)

        button_browse_one = tk.Button(frame_browse_one, text="Browse A File", command=self.file_dialog,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_one.pack(pady=5, padx=100, side="left", expand=True, fill=X)

        frame_text = tk.Frame(self)
        frame_text.pack(expand=True)

        label_txt = tk.Label(frame_text, text="Text", width=7)
        label_txt.pack(side=LEFT, anchor=N, padx=3)
        button_browse = tk.Button(frame_text, text="Set Text", command=self.get_text, font=('Arial', 10),
                                  cursor="hand2", width=14)
        button_browse.pack(side=BOTTOM, padx=10, pady=10, anchor=E)

        self.txt = tk.Text(frame_text)
        self.txt.configure(height=10)
        self.txt.pack(side=LEFT, padx=10)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        frame_space = Frame(self)
        frame_space.pack(fill=X, pady=15)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            if path1 == "" or text == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Audio path does not exists!')
                    self.path_one.delete(0, 'end')
                else:
                    global dictionary_positions
                    image_audio = make_new_image(path1)
                    img, pozitii_chr = load_text_in_audio(text, image_audio)
                    self.path_one.delete(0, 'end')
                    self.txt.delete('1.0', 'end')

                    cv2.imwrite('text_in_audio.png', img)
                    dictionary_positions = pozitii_chr
                    lista_px = extract_list(img)
                    scaled = np.int16(lista_px/np.max(np.abs(lista_px)) * 32767)
                    sf.write('text_in_audio.wav', scaled, 44100)

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path1 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Image path does not exists!')
                    self.path_one.delete(0, 'end')
                else:
                    image = cv2.imread(path1, cv2.IMREAD_COLOR)
                    extracted_text = unload_text_from_audio(image, dictionary_positions)
                    self.path_one.delete(0, 'end')
                    messagebox.showinfo("Text from audio", extracted_text)

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageThree), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path_one.get().replace('\\', '\\\\')

    def get_text(self):
        global text
        text = self.txt.get("1.0", "end-1c")
        if len(text) > 255:
            self.txt.delete('1.0', 'end')
            messagebox.showinfo("Error", "Length of the text should be lower that 256 character!")

    filename = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An Audio or An Image",
                                                   filetype=(("wav files", "*.wav"), ("mp3 files", "*.mp3"),
                                                             ("png files", "*.png")))
        self.path_one.delete(0, END)
        self.path_one.insert(0, self.filename)
        self.get_path()


class MainPageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        image = Image.open("c3.jpg")
        photo = ImageTk.PhotoImage(image)
        img = tk.Label(self, image=photo)
        img.image = photo
        img.place(x=0, y=0)

        label = tk.Label(self, text='Menu', font=title_font, fg='#d4cc79', bg="#354966")
        label.pack(pady=40, padx=30, side="top", fill="both")

        button1 = tk.Button(self, text='Hide image in video', width=15,
                            command=lambda: controller.show_page(PageFourV1), bg="#f1f5d3", font=font, cursor="hand2")
        button1.pack(pady=10, padx=30, side="top", fill="both")

        button2 = tk.Button(self, text='Hide text in video', width=15,
                            command=lambda: controller.show_page(PageFourV2), bg="#f1f5d3", font=font, cursor="hand2")
        button2.pack(pady=10, padx=30, side="top", fill="both")

        button_back = tk.Button(self, text='Back to Home', width=15, command=lambda: controller.
                                show_page(MainPage), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, padx=60, expand=True, fill=X)


class PageFourV1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Hide image in video', font=title_font)
        label.pack(pady=30, padx=20, side="top", fill='both')

        frame_path_one = tk.Frame(self)
        frame_path_one.pack(fill=X)

        label_path_one = tk.Label(frame_path_one, text="Path Image to hide", width=15)
        label_path_one.pack(side=LEFT, padx=5, pady=5)

        self.path_one = Entry(frame_path_one)
        self.path_one.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_one, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=5)
        button_browse.pack(pady=10, padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse_one = tk.Frame(self)
        frame_browse_one.pack(fill=X)

        label_or_one = tk.Label(frame_browse_one, text="or", width=10)
        label_or_one.pack(side=TOP, padx=5)

        button_browse_one = tk.Button(frame_browse_one, text="Browse A File", command=self.file_dialog,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_one.pack(pady=5, padx=100, side="left", expand=True, fill=X)

        frame_path_two = tk.Frame(self)
        frame_path_two.pack(fill=X)

        label_path_two = tk.Label(frame_path_two, text="Path Video", width=15)
        label_path_two.pack(side=LEFT, padx=5, pady=5)

        self.path_two = Entry(frame_path_two)
        self.path_two.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_two, text="Set Path", command=self.get_path_two, font=('Arial', 10),
                                  cursor="hand2", width=5)
        button_browse.pack(pady=10, padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse_two = tk.Frame(self)
        frame_browse_two.pack(fill=X)

        label_or_two = tk.Label(frame_browse_two, text="or", width=10)
        label_or_two.pack(side=TOP, padx=5)

        button_browse_two = tk.Button(frame_browse_two, text="Browse A File", command=self.file_dialog_two,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_two.pack(pady=5, padx=100, side="left", expand=True, fill=X)

        frame_scale = Frame(self)
        frame_scale.pack(fill=X, pady=10)
        label_scale = tk.Label(frame_scale, text="Number of byte", width=15)
        label_scale.pack(side=LEFT, pady=10, padx=5)

        scale = Scale(frame_scale, from_=1, to=7, orient=HORIZONTAL, tickinterval=1)
        scale.pack(side=LEFT, padx=5, expand=True, fill=X)

        def set_values():
            global bite
            bite = scale.get()

        button = Button(frame_scale, text="Set value", command=set_values, font=('Arial', 10), cursor="hand2", width=10)
        button.pack(side=LEFT, padx=20)

        frame_space = Frame(self)
        frame_space.pack(fill=X, pady=25)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            if path1 == "" or path2 == "" or (bite < 1 or bite > 7):
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Image path does not exists!')
                    self.path_one.delete(0, 'end')
                if os.path.exists(path2) is False:
                    messagebox.showinfo("Error", 'Video path does not exists!')
                    self.path_two.delete(0, 'end')
                elif os.path.exists(path1) and os.path.exists(path2):
                    global size_img
                    global number
                    image_to_hide = cv2.imread(path1, cv2.IMREAD_COLOR)
                    size_img = image_to_hide.shape[:3]
                    video = cv2.VideoCapture(path2)
                    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                    random_frame = random.randint(0, frame_count//2)
                    number = random_frame
                    print("At this position will be the image", random_frame)

                    video.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
                    _, image = video.read()
                    return_image = hide_image_in_frame(image, image_to_hide, bite)
                    cv2.imwrite("image_in_video.png", return_image)

                    change_frame_in_video(path2, return_image, random_frame)
                    self.path_one.delete(0, 'end')
                    self.path_two.delete(0, 'end')

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path2 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path2) is False:
                    messagebox.showinfo("Error", 'Video path does not exists!')
                    self.path_two.delete(0, 'end')
                else:
                    return_image = cv2.imread("image_in_video.png", cv2.IMREAD_COLOR)
                    unload_image_from_video(path2, return_image, number, bite, size_img)
                    self.path_two.delete(0, 'end')

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageFour), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path_one.get().replace('\\', '\\\\')

    def get_path_two(self):
        global path2
        path2 = self.path_two.get().replace('\\', '\\\\')

    filename = ""
    filename1 = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                   filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path_one.delete(0, END)
        self.path_one.insert(0, self.filename)
        self.get_path()

    def file_dialog_two(self):
        self.filename1 = filedialog.askopenfilename(initialdir="/", title="Select A Video",
                                                    filetype=(("mp4 files", "*.mp4"), ("avi files", "*.avi")))
        self.path_two.delete(0, END)
        self.path_two.insert(0, self.filename1)
        self.get_path_two()


class PageFourV2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text='Hide text in video', font=title_font)
        label.pack(pady=30, padx=20, side="top", fill='both')

        frame_path = tk.Frame(self)
        frame_path.pack(fill=X)

        label_path = tk.Label(frame_path, text="Path Video", width=8)
        label_path.pack(side=LEFT, padx=5, pady=5)

        self.path = Entry(frame_path)
        self.path.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=3)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse = tk.Frame(self)
        frame_browse.pack(fill=X)

        label_or = tk.Label(frame_browse, text="or", width=10)
        label_or.pack(side=TOP, padx=5)

        button_browse = tk.Button(frame_browse, text="Browse A File", command=self.file_dialog, font=('Arial', 10),
                                  cursor="hand2", width=5)
        button_browse.pack(pady=10, padx=100, side="left", expand=True, fill=X)

        frame_text = tk.Frame(self)
        frame_text.pack(expand=True)

        label_txt = tk.Label(frame_text, text="Text", width=7)
        label_txt.pack(side=LEFT, anchor=N, padx=3)
        button_browse = tk.Button(frame_text, text="Set Text", command=self.get_text, font=('Arial', 10),
                                  cursor="hand2", width=14)
        button_browse.pack(side=BOTTOM, padx=10, pady=10, anchor=E)

        self.txt = tk.Text(frame_text)
        self.txt.configure(height=10)
        self.txt.pack(side=LEFT, padx=10)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            if path1 == "" or text == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Video path does not exists!')
                    self.path.delete(0, 'end')
                else:
                    global dictionary_positions
                    global number
                    video = cv2.VideoCapture(path1)
                    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                    random_frame = random.randint(0, frame_count // 2)
                    number = random_frame
                    print("At this position will be the text", random_frame)

                    video.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
                    _, image = video.read()
                    img, pozitii_chr = load_text_in_video(text, image)
                    cv2.imwrite("text_in_video.png", img)
                    dictionary_positions = pozitii_chr

                    change_frame_in_video(path1, img, random_frame)
                    self.path.delete(0, 'end')
                    self.txt.delete('1.0', 'end')

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path1 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Video path does not exists!')
                    self.path.delete(0, 'end')
                else:
                    img = cv2.imread("text_in_video.png", cv2.IMREAD_COLOR)
                    extracted_text = unload_text_from_video(path1, img, dictionary_positions, number)
                    self.path.delete(0, 'end')
                    messagebox.showinfo("Message", extracted_text)

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageFour), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path.get().replace('\\', '\\\\')

    def get_text(self):
        global text
        text = self.txt.get("1.0", "end-1c")
        if len(text) > 255:
            self.txt.delete('1.0', 'end')
            messagebox.showinfo("Error", "Length of the text should be lower that 256 character!")

    filename = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A Video or An Image",
                                                   filetype=(("mp4 files", "*.mp4"), ("avi files", "*.avi"),
                                                             ("png files", "*.png")))
        self.path.delete(0, END)
        self.path.insert(0, self.filename)
        self.get_path()


class MainPageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        image = Image.open("c3.jpg")
        photo = ImageTk.PhotoImage(image)
        img = tk.Label(self, image=photo)
        img.image = photo
        img.place(x=0, y=0)

        label = tk.Label(self, text='Menu', font=title_font, fg='#d4cc79', bg="#354966")
        label.pack(pady=40, padx=30, side="top", fill="both")

        button1 = tk.Button(self, text='Add image logo to image', width=15,
                            command=lambda: controller.show_page(PageFiveV1), bg="#f1f5d3", font=font, cursor="hand2")
        button1.pack(pady=10, padx=30, side="top", fill="both")

        button2 = tk.Button(self, text='Add text logo to image', width=15,
                            command=lambda: controller.show_page(PageFiveV2), bg="#f1f5d3", font=font, cursor="hand2")
        button2.pack(pady=10, padx=30, side="top", fill="both")

        button3 = tk.Button(self, text='Add image logo to video', width=15,
                            command=lambda: controller.show_page(PageFiveV3), bg="#f1f5d3", font=font, cursor="hand2")
        button3.pack(pady=10, padx=30, side="top", fill="both")

        button4 = tk.Button(self, text='Add text logo to video', width=15,
                            command=lambda: controller.show_page(PageFiveV4), bg="#f1f5d3", font=font, cursor="hand2")
        button4.pack(pady=10, padx=30, side="top", fill="both")

        button_back = tk.Button(self, text='Back to Home', width=15, command=lambda: controller.
                                show_page(MainPage), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, padx=60, expand=True, fill=X)


class PageFiveV1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Add image logo to image', font=title_font)
        label.pack(pady=15, padx=10)

        frame_path_one = tk.Frame(self)
        frame_path_one.pack(fill=X)

        label_path_one = tk.Label(frame_path_one, text="Path Image", width=8)
        label_path_one.pack(side=LEFT, padx=5, pady=5)

        self.path_one = Entry(frame_path_one)
        self.path_one.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_one, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=1)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse_one = tk.Frame(self)
        frame_browse_one.pack(fill=X)

        label_or_one = tk.Label(frame_browse_one, text="or", width=10)
        label_or_one.pack(side=TOP, padx=5)

        button_browse_one = tk.Button(frame_browse_one, text="Browse A File", command=self.file_dialog,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_one.pack(pady=5, padx=150, side="left", expand=True, fill=X)

        frame_path_two = tk.Frame(self)
        frame_path_two.pack(fill=X)

        label_path_two = tk.Label(frame_path_two, text="Path logo", width=8)
        label_path_two.pack(side=LEFT, padx=5, pady=5)

        self.path_two = Entry(frame_path_two)
        self.path_two.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_two, text="Set Path", command=self.get_path_two, font=('Arial', 10),
                                  cursor="hand2", width=1)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse_two = tk.Frame(self)
        frame_browse_two.pack(fill=X)

        label_or_two = tk.Label(frame_browse_two, text="or", width=10)
        label_or_two.pack(side=TOP, padx=5)

        button_browse_two = tk.Button(frame_browse_two, text="Browse A File", command=self.file_dialog_two,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_two.pack(pady=5, padx=150, side="left", expand=True, fill=X)

        frame_radio = tk.Frame(self)
        frame_radio.pack(fill=X)

        v = tk.IntVar()

        tk.Label(frame_radio, text="""Choose position for the text:""", pady=10, padx=5).pack(anchor=tk.W)
        tk.Radiobutton(frame_radio, text="Top Left", padx=20, variable=v, value=1).pack(anchor=tk.W, padx=10)
        tk.Radiobutton(frame_radio, text="Top Right", padx=20, variable=v, value=2).pack(anchor=tk.W, padx=10)
        tk.Radiobutton(frame_radio, text="Center", padx=20, variable=v, value=3).pack(anchor=tk.W, padx=10)
        tk.Radiobutton(frame_radio, text="Bottom Right", padx=20, variable=v, value=4).pack(anchor=tk.W, padx=10)
        tk.Radiobutton(frame_radio, text="Bottom Left", padx=20, variable=v, value=5).pack(anchor=tk.W, padx=10)

        frame_scale = Frame(self)
        frame_scale.pack(fill=X, pady=10)
        label_scale = tk.Label(frame_scale, text="Alpha value:", width=11)
        label_scale.pack(side=LEFT, pady=10, padx=5)

        scale = Scale(frame_scale, from_=0, to=1, orient=HORIZONTAL, resolution=0.1)
        scale.pack(side=LEFT, padx=5, expand=True, fill=X)

        def set_values():
            global bite
            bite = scale.get()

        button = Button(frame_scale, text="Set alpha", command=set_values, font=('Arial', 10), cursor="hand2", width=9)
        button.pack(side=LEFT, padx=10, pady=10)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            if path1 == "" or path2 == "" or v.get() not in [1, 2, 3, 4, 5] or (bite < 0 or bite > 1):
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Cover image path does not exists!')
                    self.path_one.delete(0, 'end')
                elif os.path.exists(path2) is False:
                    messagebox.showinfo("Error", 'Logo path does not exists!')
                    self.path_two.delete(0, 'end')
                elif os.path.exists(path1) and os.path.exists(path2):
                    cover_image = cv2.imread(path1, cv2.IMREAD_COLOR)
                    row_cover, col_cover = cover_image.shape[:2]
                    logo = cv2.imread(path2, cv2.IMREAD_COLOR)
                    row_logo, col_logo = logo.shape[:2]
                    if row_logo//5 > row_cover or col_logo//5 > col_cover:
                        self.path_one.delete(0, 'end')
                        self.path_two.delete(0, 'end')
                        messagebox.showinfo("Message", 'Logo image should not be larger than cover image!')
                    else:
                        global poz_x
                        global poz_y
                        if v.get() == 1:            # top left
                            poz_x = 5
                            poz_y = 5
                        elif v.get() == 2:          # top right
                            poz_x = 5
                            poz_y = col_cover - col_logo//5 - 5
                        elif v.get() == 3:          # center
                            poz_x = row_cover//2 - (row_logo//5)//2 - 5
                            poz_y = col_cover//2 - (col_logo//5)//2 - 5
                        elif v.get() == 4:          # bottom right
                            poz_x = row_cover - row_logo//5 - 15
                            poz_y = col_cover - row_logo//5 - 15
                        else:                       # bottom left
                            poz_x = row_cover - row_logo // 5 - 15
                            poz_y = 15
                        add_watermark_img(path1, path2, bite, poz_x, poz_y)
                        self.path_one.delete(0, END)
                        self.path_two.delete(0, END)

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path1 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Modified image path does not exists!')
                    self.path_one.delete(0, 'end')
                else:
                    remove_watermark_img(path1, poz_x, poz_y)
                    self.path_one.delete(0, END)

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageFive), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path_one.get().replace('\\', '\\\\')

    def get_path_two(self):
        global path2
        path2 = self.path_two.get().replace('\\', '\\\\')

    filename = ""
    filename1 = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                   filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path_one.delete(0, END)
        self.path_one.insert(0, self.filename)
        self.get_path()

    def file_dialog_two(self):
        self.filename1 = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                    filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path_two.delete(0, END)
        self.path_two.insert(0, self.filename1)
        self.get_path_two()


class PageFiveV2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Add text logo to image', font=title_font)
        label.pack(pady=15, padx=10)

        frame_path = tk.Frame(self)
        frame_path.pack(fill=X)

        label_path = tk.Label(frame_path, text="Path Image", width=8)
        label_path.pack(side=LEFT, padx=5, pady=5)

        self.path = Entry(frame_path, bd=1, font=('Arial', 12))
        self.path.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=1)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse = tk.Frame(self)
        frame_browse.pack(fill=X)

        label_or = tk.Label(frame_browse, text="or", width=10)
        label_or.pack(side=TOP, padx=5)

        button_browse = tk.Button(frame_browse, text="Browse A File", command=self.file_dialog, font=('Arial', 10),
                                  cursor="hand2", width=5)
        button_browse.pack(pady=10, padx=150, side="left", expand=True, fill=X)

        frame_text = tk.Frame(self)
        frame_text.pack(expand=True)

        label_txt = tk.Label(frame_text, text="Text", width=7)
        label_txt.pack(side=LEFT, anchor=N, padx=5)
        button_browse = tk.Button(frame_text, text="Set Text", command=self.get_text, font=('Arial', 10),
                                  cursor="hand2", width=9)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        self.txt = tk.Text(frame_text)
        self.txt.configure(height=3, font=('Arial', 12))
        self.txt.pack(side=LEFT, padx=10)

        def delete_default_text(event):
            if self.color.get() == "B, G, R":
                self.color.delete(0, 'end')
                self.color.insert(0, '')

        frame_color = tk.Frame(self)
        frame_color.pack(fill=X, pady=3)

        label_color = tk.Label(frame_color, text="Text color", width=7)
        label_color.pack(side=LEFT, anchor=N, padx=5)

        self.color = Entry(frame_color, bd=1, font=('Arial', 12))
        self.color.pack(side=LEFT, fill=X, padx=10, expand=True)
        self.color.insert(0, "B, G, R")
        self.color.bind('<FocusIn>', delete_default_text)

        button_browse = tk.Button(frame_color, text="Set Color", command=self.get_color, font=('Arial', 10),
                                  cursor="hand2", width=1)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_radio = tk.Frame(self)
        frame_radio.pack(fill=X)

        v = tk.IntVar()

        tk.Label(frame_radio, text="""Choose position for the text:""", pady=10, padx=5).pack(anchor=tk.W)
        tk.Radiobutton(frame_radio, text="Top Left      ", padx=20, variable=v, value=1).pack(padx=6, side="left",
                                                                                              expand=True, fill=X)
        tk.Radiobutton(frame_radio, text="Top Right      ", padx=20, variable=v, value=2).pack(padx=6, side="right",
                                                                                               expand=True, fill=X)

        frame_radio_1 = tk.Frame(self)
        frame_radio_1.pack(fill=X)
        tk.Radiobutton(frame_radio_1, text="Bottom Left", padx=20, variable=v, value=4).pack(padx=6, side="left",
                                                                                             expand=True, fill=X)
        tk.Radiobutton(frame_radio_1, text="Bottom Right", padx=20, variable=v, value=5).pack(padx=6, side="right",
                                                                                              expand=True, fill=X)

        frame_radio_2 = tk.Frame(self)
        frame_radio_2.pack(fill=X, padx=5)
        tk.Radiobutton(frame_radio_2, text="Center", padx=20, variable=v, value=3).pack(padx=10, side="left",
                                                                                        expand=True, fill=X)

        w = tk.IntVar()
        frame_radio2 = tk.Frame(self)
        frame_radio2.pack(fill=X)
        tk.Label(frame_radio2, text="""Save mask""", pady=10, padx=5).pack(anchor=tk.W)
        tk.Radiobutton(frame_radio2, text="Save", padx=20, variable=w, value=1).pack(pady=6, padx=10, side="left",
                                                                                     expand=True, fill=X)
        tk.Radiobutton(frame_radio2, text="Don't save", padx=20, variable=w, value=0).pack(pady=6, padx=10,
                                                                                           side="right", expand=True,
                                                                                           fill=X)

        frame_scale = Frame(self)
        frame_scale.pack(fill=X, pady=10)
        label_scale = tk.Label(frame_scale, text="Alpha value:", width=11)
        label_scale.pack(side=LEFT, pady=10, padx=5)

        scale = Scale(frame_scale, from_=0, to=1, orient=HORIZONTAL, resolution=0.1)
        scale.pack(side=LEFT, padx=5, expand=True, fill=X)

        def set_values():
            global bite
            bite = scale.get()

        button = Button(frame_scale, text="Set alpha", command=set_values, font=('Arial', 10), cursor="hand2", width=9)
        button.pack(side=LEFT, padx=10, pady=10)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            if color == "" or path1 == "" or text == "" or v.get() not in [1, 2, 3, 4, 5] or w.get() not in [1, 0] or \
                    (bite < 0 or bite > 1):
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Image path does not exists!')
                    self.path.delete(0, 'end')
                else:
                    list_color = list()
                    for elem in color.replace("(", "").replace(")", "").split(","):
                        list_color.append(int(elem))
                    create_txt_image(text, list_color, w.get(), 1)
                    mask = cv2.imread("mask.png")
                    row_mask, col_mask = mask.shape[:2]
                    cover_image = cv2.imread(path1)
                    row_cover, col_cover = cover_image.shape[:2]
                    if row_mask > row_cover or col_mask > col_cover:
                        self.path.delete(0, 'end')
                        self.txt.delete('1.0', 'end')
                        messagebox.showinfo("Message", 'Mask image from the text should'
                                                       ' not be larger than cover image!')
                    else:
                        global poz_x
                        global poz_y
                        if v.get() == 1:            # top left
                            poz_x = 5
                            poz_y = 5
                        elif v.get() == 2:          # top right
                            poz_x = 5
                            poz_y = col_cover - col_mask - 5
                        elif v.get() == 3:          # center
                            poz_x = row_cover//2 - row_mask//2 - 5
                            poz_y = col_cover//2 - col_mask//2 - 5
                        elif v.get() == 4:          # bottom left
                            poz_x = row_cover - row_mask - 5
                            poz_y = 5
                        else:                       # bottom right
                            poz_x = row_cover - row_mask - 5
                            poz_y = col_cover - col_mask - 5
                        #
                        # print("-------->", poz_x, poz_y)
                        add_watermark_text(path1, text, list_color, w.get(), bite, poz_x, poz_y)
                        self.path.delete(0, END)
                        self.txt.delete('1.0', 'end')
                        self.color.delete(0, 'end')
                        self.color.insert(0, "B, G, R")
                        self.color.bind('<FocusIn>', delete_default_text)

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path1 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Modified image path does not exists!')
                    self.path.delete(0, 'end')
                else:
                    remove_watermark_text(path1, poz_x, poz_y)
                    self.path.delete(0, END)

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageFive), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path.get().replace('\\', '\\\\')

    def get_color(self):
        global color
        color = self.color.get()
        color = color.replace(" ", "")
        pattern = r"(\d+),(\d+),(\d+)"
        match = re.search(pattern, color)
        if match is None:
            self.color.delete(0, 'end')
            messagebox.showinfo("Info", 'Incorrect input.\nThe input should be integer values.')
        else:
            search = re.search(pattern, color, re.IGNORECASE)
            if int(search.group(1)) > 255 or int(search.group(2)) > 255 or int(search.group(3)) > 255:
                self.color.delete(0, 'end')
                messagebox.showinfo("Info", 'Values of R, G, B should be between 0 and 255!')

    def get_text(self):
        global text
        text = self.txt.get("1.0", "end-1c")
        if len(text) > 255:
            self.txt.delete('1.0', 'end')
            messagebox.showinfo("Error", "Length of the text should be lower that 256 character!")

    filename = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                   filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path.delete(0, END)
        self.path.insert(0, self.filename)
        self.get_path()


class PageFiveV3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Add image logo to video', font=title_font)
        label.pack(pady=15, padx=10)

        frame_path_one = tk.Frame(self)
        frame_path_one.pack(fill=X)

        label_path_one = tk.Label(frame_path_one, text="Path Image", width=8)
        label_path_one.pack(side=LEFT, padx=5, pady=5)

        self.path_one = Entry(frame_path_one)
        self.path_one.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_one, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=1)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse_one = tk.Frame(self)
        frame_browse_one.pack(fill=X)

        label_or_one = tk.Label(frame_browse_one, text="or", width=10)
        label_or_one.pack(side=TOP, padx=5)

        button_browse_one = tk.Button(frame_browse_one, text="Browse A File", command=self.file_dialog,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_one.pack(pady=5, padx=150, side="left", expand=True, fill=X)

        frame_path_two = tk.Frame(self)
        frame_path_two.pack(fill=X)

        label_path_two = tk.Label(frame_path_two, text="Path Video", width=8)
        label_path_two.pack(side=LEFT, padx=5, pady=5)

        self.path_two = Entry(frame_path_two)
        self.path_two.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path_two, text="Set Path", command=self.get_path_two, font=('Arial', 10),
                                  cursor="hand2", width=1)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse_two = tk.Frame(self)
        frame_browse_two.pack(fill=X)

        label_or_two = tk.Label(frame_browse_two, text="or", width=10)
        label_or_two.pack(side=TOP, padx=5)

        button_browse_two = tk.Button(frame_browse_two, text="Browse A File", command=self.file_dialog_two,
                                      font=('Arial', 10), cursor="hand2", width=5)
        button_browse_two.pack(pady=5, padx=150, side="left", expand=True, fill=X)

        frame_radio = tk.Frame(self)
        frame_radio.pack(fill=X)

        v = tk.IntVar()

        tk.Label(frame_radio, text="""Choose position for the text:""", pady=10, padx=5).pack(anchor=tk.W)
        tk.Radiobutton(frame_radio, text="Top Left", padx=20, variable=v, value=1).pack(anchor=tk.W, padx=10)
        tk.Radiobutton(frame_radio, text="Top Right", padx=20, variable=v, value=2).pack(anchor=tk.W, padx=10)
        tk.Radiobutton(frame_radio, text="Center", padx=20, variable=v, value=3).pack(anchor=tk.W, padx=10)
        tk.Radiobutton(frame_radio, text="Bottom Right", padx=20, variable=v, value=4).pack(anchor=tk.W, padx=10)
        tk.Radiobutton(frame_radio, text="Bottom Left", padx=20, variable=v, value=5).pack(anchor=tk.W, padx=10)

        frame_scale = Frame(self)
        frame_scale.pack(fill=X, pady=10)
        label_scale = tk.Label(frame_scale, text="Alpha value:", width=11)
        label_scale.pack(side=LEFT, pady=10, padx=5)

        scale = Scale(frame_scale, from_=0, to=1, orient=HORIZONTAL, resolution=0.1)
        scale.pack(side=LEFT, padx=5, expand=True, fill=X)

        def set_values():
            global bite
            bite = scale.get()

        button = Button(frame_scale, text="Set alpha", command=set_values, font=('Arial', 10), cursor="hand2", width=9)
        button.pack(side=LEFT, padx=10, pady=10)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            if path1 == "" or path2 == "" or v.get() not in [1, 2, 3, 4, 5] or (bite < 0 or bite > 1):
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Image path does not exists!')
                    self.path_one.delete(0, 'end')
                elif os.path.exists(path2) is False:
                    messagebox.showinfo("Error", 'Video path does not exists!')
                    self.path_two.delete(0, 'end')
                elif os.path.exists(path1) and os.path.exists(path2):
                    video = cv2.VideoCapture(path2)
                    row_cover = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    col_cover = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
                    logo = cv2.imread(path1, cv2.IMREAD_COLOR)
                    row_logo, col_logo = logo.shape[:2]
                    if row_logo // 5 > row_cover or col_logo // 5 > col_cover:
                        self.path_one.delete(0, 'end')
                        self.path_two.delete(0, 'end')
                        messagebox.showinfo("Message", 'Logo image should not be larger than cover image!')
                    else:
                        global poz_x
                        global poz_y
                        if v.get() == 1:            # top left
                            poz_x = 5
                            poz_y = 5
                        elif v.get() == 2:          # top right
                            poz_x = 5
                            poz_y = col_cover - col_logo//5 - 5
                        elif v.get() == 3:          # center
                            poz_x = row_cover//2 - (row_logo//5)//2 - 5
                            poz_y = col_cover//2 - (col_logo//5)//2 - 5
                        elif v.get() == 4:          # bottom right
                            poz_x = row_cover - row_logo//5 - 50
                            poz_y = col_cover - row_logo//5 - 50
                        else:                       # bottom left
                            poz_x = row_cover - row_logo // 5 - 50
                            poz_y = 15
                        add_watermark_image_video(path1, path2, poz_x, poz_y, bite)
                        self.path_one.delete(0, END)
                        self.path_two.delete(0, END)

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path2 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path2) is False:
                    messagebox.showinfo("Error", 'Modified video path does not exists!')
                    self.path_two.delete(0, 'end')
                else:
                    remove_watermark_image_video(path2, poz_x, poz_y)
                    self.path_two.delete(0, END)

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageFive), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path_one.get().replace('\\', '\\\\')

    def get_path_two(self):
        global path2
        path2 = self.path_two.get().replace('\\', '\\\\')

    filename = ""
    filename1 = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                   filetype=(("jpeg files", "*.jpg"), ("png files", "*.png")))
        self.path_one.delete(0, END)
        self.path_one.insert(0, self.filename)
        self.get_path()

    def file_dialog_two(self):
        self.filename1 = filedialog.askopenfilename(initialdir="/", title="Select A Video",
                                                    filetype=(("mp4 files", "*.mp4"), ("avi files", "*.avi")))
        self.path_two.delete(0, END)
        self.path_two.insert(0, self.filename1)
        self.get_path_two()


class PageFiveV4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Add text logo in video', font=title_font)
        label.pack(pady=15, padx=10)

        frame_path = tk.Frame(self)
        frame_path.pack(fill=X)

        label_path = tk.Label(frame_path, text="Path Video", width=7)
        label_path.pack(side=LEFT, padx=5, pady=5)

        self.path = Entry(frame_path, bd=1, font=('Arial', 12))
        self.path.pack(side=LEFT, fill=X, padx=10, expand=True)

        button_browse = tk.Button(frame_path, text="Set Path", command=self.get_path, font=('Arial', 10),
                                  cursor="hand2", width=1)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_browse = tk.Frame(self)
        frame_browse.pack(fill=X)

        label_or = tk.Label(frame_browse, text="or", width=10)
        label_or.pack(side=TOP, padx=5)

        button_browse = tk.Button(frame_browse, text="Browse A File", command=self.file_dialog, font=('Arial', 10),
                                  cursor="hand2", width=5)
        button_browse.pack(pady=10, padx=150, side="left", expand=True, fill=X)

        frame_text = tk.Frame(self)
        frame_text.pack(expand=True)

        label_txt = tk.Label(frame_text, text="Text", width=7)
        label_txt.pack(side=LEFT, anchor=N, padx=5)
        button_browse = tk.Button(frame_text, text="Set Text", command=self.get_text, font=('Arial', 10),
                                  cursor="hand2", width=9)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        self.txt = tk.Text(frame_text)
        self.txt.configure(height=3)
        self.txt.pack(side=LEFT, padx=10)

        def delete_default_text(event):
            if self.color.get() == "B, G, R":
                self.color.delete(0, 'end')
                self.color.insert(0, '')

        frame_color = tk.Frame(self)
        frame_color.pack(fill=X, pady=3)

        label_color = tk.Label(frame_color, text="Text color", width=7)
        label_color.pack(side=LEFT, anchor=N, padx=5)

        self.color = Entry(frame_color, bd=1, font=('Arial', 12))
        self.color.pack(side=LEFT, fill=X, padx=10, expand=True)
        self.color.insert(0, "B, G, R")
        self.color.bind('<FocusIn>', delete_default_text)

        button_browse = tk.Button(frame_color, text="Set Color", command=self.get_color, font=('Arial', 10),
                                  cursor="hand2", width=1)
        button_browse.pack(padx=10, side=RIGHT, expand=True, fill=X)

        frame_radio = tk.Frame(self)
        frame_radio.pack(fill=X)

        v = tk.IntVar()

        tk.Label(frame_radio, text="""Choose position for the text:""", pady=10, padx=5).pack(anchor=tk.W)
        tk.Radiobutton(frame_radio, text="Top Left      ", padx=20, variable=v, value=1).pack(padx=6, side="left",
                                                                                              expand=True, fill=X)
        tk.Radiobutton(frame_radio, text="Top Right      ", padx=20, variable=v, value=2).pack(padx=6, side="right",
                                                                                               expand=True, fill=X)

        frame_radio_1 = tk.Frame(self)
        frame_radio_1.pack(fill=X)
        tk.Radiobutton(frame_radio_1, text="Bottom Left", padx=20, variable=v, value=4).pack(padx=6, side="left",
                                                                                             expand=True, fill=X)
        tk.Radiobutton(frame_radio_1, text="Bottom Right", padx=20, variable=v, value=5).pack(padx=6, side="right",
                                                                                              expand=True, fill=X)

        frame_radio_2 = tk.Frame(self)
        frame_radio_2.pack(fill=X, padx=5)
        tk.Radiobutton(frame_radio_2, text="Center", padx=20, variable=v, value=3).pack(padx=10, side="left",
                                                                                        expand=True, fill=X)

        w = tk.IntVar()
        frame_radio2 = tk.Frame(self)
        frame_radio2.pack(fill=X)
        tk.Label(frame_radio2, text="""Save mask""", pady=10, padx=5).pack(anchor=tk.W)
        tk.Radiobutton(frame_radio2, text="Save", padx=20, variable=w, value=1).pack(pady=6, padx=10, side="left",
                                                                                     expand=True, fill=X)
        tk.Radiobutton(frame_radio2, text="Don't save", padx=20, variable=w, value=0).pack(pady=6, padx=10,
                                                                                           side="right", expand=True,
                                                                                           fill=X)

        frame_scale = Frame(self)
        frame_scale.pack(fill=X, pady=10)
        label_scale = tk.Label(frame_scale, text="Alpha value:", width=11)
        label_scale.pack(side=LEFT, pady=10, padx=5)

        scale = Scale(frame_scale, from_=0, to=1, orient=HORIZONTAL, resolution=0.1)
        scale.pack(side=LEFT, padx=5, expand=True, fill=X)

        def set_values():
            global bite
            bite = scale.get()

        button = Button(frame_scale, text="Set alpha", command=set_values, font=('Arial', 10), cursor="hand2", width=9)
        button.pack(side=LEFT, padx=10, pady=10)

        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        def final_load():
            list_color = list()
            if color == "" or path1 == "" or text == "" or (bite < 0 or bite > 1) or v.get() not in [1, 2, 3, 4, 5] \
                    or w.get() not in [1, 0]:
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Video path does not exists!')
                    self.path.delete(0, 'end')
                else:
                    for elem in color.replace("(", "").replace(")", "").split(","):
                        list_color.append(int(elem))
                    create_txt_image(text, list_color, w.get(), 0)
                    mask = cv2.imread("mask.png")
                    row_mask, col_mask = mask.shape[:2]
                    video = cv2.VideoCapture(path1)
                    row_cover = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    col_cover = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
                    if row_mask > row_cover or col_mask > col_cover:
                        self.path.delete(0, 'end')
                        self.txt.delete('1.0', 'end')
                        messagebox.showinfo("Message", 'Mask image from the text should'
                                                       ' not be larger than cover image!')
                    else:
                        global poz_x
                        global poz_y

                        if v.get() == 1:  # top left
                            poz_x = 5
                            poz_y = 5
                        elif v.get() == 2:  # top right
                            poz_x = 5
                            poz_y = col_cover - col_mask - 5
                        elif v.get() == 3:  # center
                            poz_x = row_cover // 2 - row_mask // 2 - 5
                            poz_y = col_cover // 2 - col_mask // 2 - 5
                        elif v.get() == 4:  # bottom left
                            poz_x = row_cover - row_mask - 50
                            poz_y = 5
                        else:  # bottom right
                            poz_x = row_cover - row_mask - 50
                            poz_y = col_cover - col_mask - 50
                        add_watermark_text_video(text, path1, poz_x, poz_y, bite, w.get(), list_color)
                        self.path.delete(0, END)
                        self.txt.delete('1.0', 'end')
                        self.color.delete(0, 'end')
                        self.color.insert(0, "B, G, R")
                        self.color.bind('<FocusIn>', delete_default_text)
                        # print("ajunge aiciiiii")

        button_load = tk.Button(frame_buttons, text='Load', width=10, command=final_load, bg="#f1f5d3", font=font,
                                cursor="hand2")
        button_load.pack(pady=10, padx=10, side="left", expand=True, fill=X)

        def final_unload():
            if path1 == "":
                messagebox.showinfo("Info", 'Incorrect input.\nThe input is not set.')
            else:
                if os.path.exists(path1) is False:
                    messagebox.showinfo("Error", 'Video path does not exists!')
                    self.path.delete(0, 'end')
                else:
                    remove_watermark_text_video(path1, poz_x, poz_y)
                    self.path.delete(0, END)

        button_unload = tk.Button(frame_buttons, text='Unload', width=10, command=final_unload, bg="#f1f5d3", font=font,
                                  cursor="hand2")
        button_unload.pack(pady=10, padx=10, side="right", expand=True, fill=X)

        frame_back = Frame(self)
        frame_back.pack(fill=X)

        button_back = tk.Button(frame_back, text='Back', width=15, command=lambda: controller.
                                show_page(MainPageFive), bg="#eed4fc", font=font, cursor="hand2")
        button_back.pack(side=BOTTOM, pady=18, padx=60, expand=True, fill=X)

    def get_path(self):
        global path1
        path1 = self.path.get().replace('\\', '\\\\')

    def get_color(self):
        global color
        color = self.color.get()
        color = color.replace(" ", "")
        pattern = r'(\d+),(\d+),(\d+)'
        match = re.search(pattern, color)
        if match is None:
            self.color.delete(0, 'end')
            messagebox.showinfo("Info", 'Incorrect input.\nThe input should be integer values.')
        else:
            search = re.search(pattern, color, re.IGNORECASE)
            if int(search.group(1)) > 255 or int(search.group(2)) > 255 or int(search.group(3)) > 255:
                self.color.delete(0, 'end')
                messagebox.showinfo("Info", 'Values of R, G, B should be between 0 and 255!')

    def get_text(self):
        global text
        text = self.txt.get("1.0", "end-1c")
        if len(text) > 255:
            self.txt.delete('1.0', 'end')
            messagebox.showinfo("Error", "Length of the text should be lower that 256 character!")

    filename = ""

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A Video",
                                                   filetype=(("mp4 files", "*.mp4"), ("avi files", "*.avi")))
        self.path.delete(0, END)
        self.path.insert(0, self.filename)
        self.get_path()


if __name__ == '__main__':
    app = Main()
    app.mainloop()

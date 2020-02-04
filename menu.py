# # import tkinter as tk
# # from tkinter.filedialog import askopenfilename
# #
# # #
# # #
# # # def donothing():
# # #     filewin = Toplevel(root)
# # #     button = Button(filewin, text="Do nothing button")
# # #     button.pack()
# # #
# # #
# # # root = Tk()
# # # root.wm_title("new menu")
# # # menubar = Menu(root)
# # # filemenu = Menu(menubar, tearoff=0)
# # # filemenu.add_command(label="New", command=donothing)
# # # filemenu.add_command(label="Open", command=donothing)
# # # filemenu.add_command(label="Save", command=donothing)
# # # filemenu.add_command(label="Save as...", command=donothing)
# # # filemenu.add_command(label="Close", command=donothing)
# # #
# # # filemenu.add_separator()
# # #
# # # filemenu.add_command(label="Exit", command=root.quit)
# # # menubar.add_cascade(label="File", menu=filemenu)
# # # editmenu = Menu(menubar, tearoff=0)
# # # editmenu.add_command(label="Undo", command=donothing)
# # #
# # # editmenu.add_separator()
# # #
# # # editmenu.add_command(label="Cut", command=donothing)
# # # editmenu.add_command(label="Copy", command=donothing)
# # # editmenu.add_command(label="Paste", command=donothing)
# # # editmenu.add_command(label="Delete", command=donothing)
# # # editmenu.add_command(label="Select All", command=donothing)
# # #
# # # menubar.add_cascade(label="Edit", menu=editmenu)
# # # helpmenu = Menu(menubar, tearoff=0)
# # # helpmenu.add_command(label="Help Index", command=donothing)
# # # helpmenu.add_command(label="About...", command=donothing)
# # # menubar.add_cascade(label="Help", menu=helpmenu)
# # #
# # # root.config(menu=menubar)
# # # root.mainloop()
# #
# # def openfile():
# #     name = askopenfilename()
# #     return name[19:]
# #
# # class MyApp(tk.Frame):
# #     def __init__(self, master=None):
# #         tk.Frame.__init__(self, master)
# #         self.master.title("MyApp")
# #
# #         self.pack(side="top", fill="both", expand=True)
# #         self.grid_rowconfigure(0, weight=1)
# #         self.grid_columnconfigure(0, weight=1)
# #
# #         top = self.winfo_toplevel()
# #         self.menubar = tk.Menu(top)
# #         top['menu'] = self.menubar
# #
# #         self.submenu = tk.Menu(self.menubar)
# #         self.menubar.add_cascade(label='Choices', menu=self.submenu)
# #
# #         self.submenu.add_command(label="Import a CSV File",
# #                                  command=self.file_openerfunction)
# #         self.submenu.add_command(label="Plot My CSV File",
# #                                  command=self.popupgraph)
# #         self.submenu.add_command(label="View MY CSV File",
# #                                  command=self.table)
# #
# #     def file_openerfunction(self):
# #         self.filename = openfile()
# #
# #     def popupgraph(self): pass
# #     def table(self): pass
# #
# # app = MyApp()
# # app.mainloop()
# import sys
# from tkinter import *
#
# root = Tk()
#
# # Insert a menu bar on the main window
# menubar = Menu(root)
# root.config(menu=menubar)
#
# # Create a menu button labeled "File" that brings up a menu
# filemenu = Menu(menubar)
# menubar.add_cascade(label='File', menu=filemenu)
#
# # Create entries in the "File" menu
# # simulated command functions that we want to invoke from our menus
# def doPrint( ):
#     print('doPrint')
# def doSave( ):
#     print('doSave')
# filemenu.add_command(label='Print', command=doPrint)
# filemenu.add_command(label='Save', command=doSave)
# filemenu.add_separator()
# filemenu.add_command(label='Quit', command=sys.exit)
# vdebug = IntVar(  )
# filemenu.add_checkbutton(label='Debug', var=vdebug)
# vlevel = IntVar(  )
# filemenu.add_radiobutton(label='Level 1', var=vlevel, value=1)
# filemenu.add_radiobutton(label='Level 2', var=vlevel, value=2)
# filemenu.add_radiobutton(label='Level 3', var=vlevel, value=3)
# root.mainloop()
from tkinter import *

# root = Tk()
# frame = Frame(root)
# frame.pack()
#
# bottomframe = Frame(root)
# bottomframe.pack( side = BOTTOM )
#
# redbutton = Button(frame, text = "Red", fg = "red")
# redbutton.pack( side = LEFT)
#
# greenbutton = Button(frame, text = "Brown", fg="brown")
# greenbutton.pack( side = LEFT )
#
# bluebutton = Button(frame, text = "Blue", fg = "blue")
# bluebutton.pack( side = LEFT )
#
# blackbutton = Button(bottomframe, text = "Black", fg = "black")
# blackbutton.pack( side = BOTTOM)
#
# root.mainloop()
#
# root = Tk()
#
# labelframe = LabelFrame(root, text="This is a LabelFrame")
# labelframe.pack(fill="both", expand="yes")
#
# left = Label(labelframe, text="Inside the LabelFrame")
# left.pack()
#
# root.mainloop()
# from tkinter import *
# from PIL import Image, ImageTk
#
# root = Tk()
#
# make_frame = LabelFrame(root, text="Sample Image", width=100, height=100)
# make_frame.pack()
#
# stim_filename = "logo.png"
#
# # create the PIL image object:
# PIL_image = Image.open(stim_filename)
#
# width = 100
# height = 100
#
# # You may prefer to use Image.thumbnail instead
# # Set use_resize to False to use Image.thumbnail
# use_resize = True
#
# if use_resize:
#     # Image.resize returns a new PIL.Image of the specified size
#     PIL_image_small = PIL_image.resize((width,height), Image.ANTIALIAS)
# else:
#     # Image.thumbnail converts the image to a thumbnail, in place
#     PIL_image_small = PIL_image
#     PIL_image_small.thumbnail((width,height), Image.ANTIALIAS)
#
# # now create the ImageTk PhotoImage:
# img = ImageTk.PhotoImage(PIL_image_small)
# in_frame = Label(make_frame, image = img)
# in_frame.pack()
#
# # root.mainloop()
# import sys, os, string, time
# import tkinter as tk
#
#
# # A Python example of drag and drop functionality within a single Tk widget.
# # The trick is in the bindings and event handler functions.
# # Tom Vrankar twv at ici.net
#
# # empirical events between dropee and target, as determined from Tk 8.0
# # down.
# # leave.
# # up, leave, enter.
#
# class CanvasDnD(tk.Frame):
#     def __init__(self, master):
#         self.master = master
#         self.loc = self.dragged = 0
#         tk.Frame.__init__(self, master)
#         canvas = tk.Canvas(self, width=256, height=256,
#                            relief=tk.RIDGE, background="white", borderwidth=1)
#         self.defaultcolor = canvas.itemcget(canvas.create_text(30, 25,
#                                                                font=("Helvetica", 14), text="Item 1", tags="DnD"),
#                                             "fill")
#         canvas.create_text(75, 75,
#                            font=("Helvetica", 14), text="Item 2", tags="DnD")
#         canvas.create_text(125, 125,
#                            font=("Helvetica", 14), text="Item 3", tags="DnD")
#         canvas.create_text(175, 175,
#                            font=("Helvetica", 14), text="Item 4", tags="DnD")
#         canvas.create_text(225, 225,
#                            font=("Helvetica", 14), text="Item 5", tags="DnD")
#         canvas.pack(expand=1, fill=tk.BOTH)
#         canvas.tag_bind("DnD", "<ButtonPress-1>", self.down)
#         canvas.tag_bind("DnD", "<ButtonRelease-1>", self.chkup)
#         canvas.tag_bind("DnD", "<Enter>", self.enter)
#         canvas.tag_bind("DnD", "<Leave>", self.leave)
#
#     def down(self, event):
#         print("Click on %s" % event.widget.itemcget(tk.CURRENT, "text"))
#         self.loc = 1
#         self.dragged = 0
#         event.widget.bind("<Motion>", self.motion)
#
#     def motion(self, event):
#         root.config(cursor="exchange")
#         event.widget.itemconfigure(tk.CURRENT, fill="blue")
#         event.widget.unbind("<Motion>")
#
#     def leave(self, event):
#         self.loc = 0
#
#     def enter(self, event):
#         self.loc = 1
#         if self.dragged == event.time:
#             self.up(event)
#
#     def chkup(self, event):
#         root.config(cursor="")
#         self.target = event.widget.find_withtag(tk.CURRENT)
#         event.widget.itemconfigure(tk.CURRENT, fill=self.defaultcolor)
#         if self.loc:  # is button released in same widget as pressed?
#             self.up(event)
#         else:
#             self.dragged = event.time
#
#     def up(self, event):
#         event.widget.unbind("<Motion>")
#         if (self.target == event.widget.find_withtag(tk.CURRENT)):
#             print("Select %s" % event.widget.itemcget(tk.CURRENT, "text"))
#         else:
#             event.widget.itemconfigure(tk.CURRENT, fill="blue")
#             self.master.update()
#             time.sleep(.1)
#             print("%s Drag-N-Dropped onto %s" % (event.widget.itemcget(self.target, "text"),event.widget.itemcget(tk.CURRENT, "text")))
#             event.widget.itemconfigure(tk.CURRENT, fill=self.defaultcolor)
#
#
# root = Tk()
# root.title("Drag-N-Drop Demo")
# CanvasDnD(root).pack()
# root.mainloop()
import tkinter as tk
# try:
#     # Python2
#     import Tkinter as tk
# except ImportError:
#     # Python3
#     import tkinter as tk
# root = tk.Tk()
# root.title('background image')
# # pick a .gif image file you have in the working directory
# fname = "t.jpg"
# bg_image = tk.PhotoImage(file=fname)
# # get the width and height of the image
# w = bg_image.width()
# h = bg_image.height()
# # size the window so the image will fill it
# root.geometry("%dx%d+50+30" % (w, h))
# cv = tk.Canvas(width=w, height=h)
# cv.pack(side='top', fill='both', expand='yes')
# cv.create_image(0, 0, image=bg_image, anchor='nw')
# # add canvas text at coordinates x=15, y=20
# # anchor='nw' implies upper left corner coordinates
# cv.create_text(15, 20, text="Python Greetings", fill="red", anchor='nw')
# # now add some button widgets
# btn1 = tk.Button(cv, text="Click")
# btn1.pack(side='left', padx=10, pady=5, anchor='sw')
# btn2 = tk.Button(cv, text="Quit", command=root.destroy)
# btn2.pack(side='left', padx=10, pady=5, anchor='sw')
# root.mainloop()
# class Example(Frame):
#
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#
#     def initUI(self):
#
#         self.master.title("Windows")
#         self.pack(fill=BOTH, expand=True)
#
#         self.columnconfigure(1, weight=1)
#         self.columnconfigure(3, pad=7)
#         self.rowconfigure(3, weight=1)
#         self.rowconfigure(5, pad=7)
#
#         lbl = Label(self, text="Windows")
#         lbl.grid(sticky=W, pady=4, padx=5)
#
#         area = Text(self)
#         area.grid(row=1, column=0, columnspan=2, rowspan=4,
#             padx=5, sticky=E+W+S+N)
#
#         abtn = Button(self, text="Activate")
#         abtn.grid(row=1, column=3)
#
#         cbtn = Button(self, text="Close")
#         cbtn.grid(row=2, column=3, pady=4)
#
#         hbtn = Button(self, text="Help")
#         hbtn.grid(row=5, column=0, padx=5)
#
#         obtn = Button(self, text="OK")
#         obtn.grid(row=5, column=3)
#
#
# def main():
#
#     root = Tk()
#     root.geometry("350x300+300+300")
#     app = Example()
#     root.mainloop()
#
#
# if __name__ == '__main__':
#     main()


from tkinter import *
from tkinter import ttk
from tkinter import filedialog
#
#
# class Root(Tk):
#     def __init__(self):
#         super(Root, self).__init__()
#         self.title("Python Tkinter Dialog Widget")
#         self.minsize(640, 400)
#         # self.wm_iconbitmap('icon.ico')
#
#         self.labelFrame = ttk.LabelFrame(self, text="Open File")
#         self.labelFrame.grid(column=0, row=1, padx=20, pady=20)
#
#         self.button()
#
#     def button(self):
#         self.button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog)
#         self.button.grid(column=1, row=1)
#
#     def fileDialog(self):
#         self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=
#         (("jpeg files", "*.jpg"), ("all files", "*.*")))
#         self.label = ttk.Label(self.labelFrame, text="")
#         self.label.grid(column=1, row=2)
#         self.label.configure(text=self.filename)
#
#
# root = Root()
# root.mainloop()
from tkinter import *

def sel():
   selection = "Value = " + str(var.get())
   label.config(text = selection)

root = Tk()
var = DoubleVar()
scale = Scale( root, variable = var, orient=HORIZONTAL)
scale.pack(anchor=CENTER)

button = Button(root, text="Get Scale Value", command=sel)
button.pack(anchor=CENTER)

label = Label(root)
label.pack()

root.mainloop()
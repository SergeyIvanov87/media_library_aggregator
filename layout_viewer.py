#!/usr/bin/python

import json
import os
import tkinter
from tkinter import ttk

import layout_loader

class MainLayoutWidget(tkinter.Tk):
    def __init__(self, json_layout):
        tkinter.Tk.__init__(self)

        name = json_layout["name"]
        self.title(f"Layout: {name}")

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        filler_frame = ttk.Frame(self, width=screen_width/2, height=screen_height/2)
        filler_frame.grid(row=0, column=0, sticky="nsew")






layout_name = input("Please specify a layout name: ")
layout_json = layout_loader.load_layout_as_json(layout_name)

root = MainLayoutWidget(layout_json)
root.mainloop()

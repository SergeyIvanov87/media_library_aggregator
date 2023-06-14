#!/usr/bin/python

import json
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk

import layout_loader


class ObjectRepresentative(tkinter.ttk.Button):
    images = []
    photo_images = []

    def __init__(self, parent, dimensions, images_list):
        self.images = [Image.open(pathToImage) for pathToImage in images_list]
        self.images = [img.resize(dimensions, Image.LANCZOS) for img in self.images]

        self.photo_images = [ImageTk.PhotoImage(image) for image in self.images]

        cur_image = self.__extract_next_photo_image__()
        tkinter.ttk.Button.__init__(
            self,
            parent,
            width=dimensions[0],
            image=cur_image,
            command=self.on_click,
        )

    def on_click(self):
        self.config(image=self.__extract_next_photo_image__())

    def __extract_next_photo_image__(self):
        next_image = self.photo_images.pop(0)
        self.photo_images.append(next_image)
        return next_image

class DescriptionRepresentative(tkinter.Toplevel):
    info_labels = []
    def __init__(self, info_files_list):
        tkinter.Toplevel.__init__(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.info_book = ttk.Notebook(self)
        self.info_book.grid_rowconfigure(0, weight=1)
        self.info_book.grid_columnconfigure(0, weight=1)
        self.info_book.pack(fill='both', expand=True)

        self.info_labels = [tkinter.Label(self.info_book, text=info) for info in info_files_list]
        for i in self.info_labels:
            i.grid_rowconfigure(0, weight=1)
            i.grid_columnconfigure(0, weight=0)
            i.grid_columnconfigure(1, weight=1)
            i.pack(fill='both', expand=True)

            self.info_book.add(i)

        self.info_book.grid(row=0, column=0)

        self.close_button = ttk.Button(self, text="Close", command=self.close)
        self.close_button.grid(row=1, column=0)

        #self.parent = parent
        self.acquire_modality()

    def close(self):
        self.release_modality()

    def __del__(self):
        self.release_modality()

    def acquire_modality(self):
        """
        make windows modal and block input for parent windows
        until this child windows interaction finishes
        """
        self.wait_visibility()
        self.grab_set()
        #self.transient(self.parent)

    def release_modality(self):
        self.grab_release()
        self.destroy()

class ObjectFrame(ttk.Frame):
    info_list = []
    sound_files_list = []
    def __init__(self, parent, dimensions, description_list, images_list, sounds_list):
        ttk.Frame.__init__(self, parent)

        self.info_list = description_list
        self.sound_files_list = sounds_list

        self.object_view = ObjectRepresentative(self, dimensions, images_list)
        self.object_view.grid(row=0, column=0)

        self.controls_frame = ttk.Frame(self)
        self.controls_frame.grid(row=1,column=0)

        # create 'Show Info' button if necessary
        if len(self.info_list):
            self.description_show_button = tkinter.ttk.Button(self.controls_frame,
                text="Show Info",
                command=self.on_description_click
            )
            self.description_show_button.grid(row=0, column=0)

        # create 'Play Sound' button if necessary
        if len(self.sound_files_list):
            self.play_sound_button = tkinter.ttk.Button(self.controls_frame,
                text="|>",
                command=self.on_play_sound_click
            )
            self.play_sound_button.grid(row=0, column=1)

    def on_description_click(self):
        description_window = DescriptionRepresentative(self.info_list)
        self.wait_window(description_window)

    def on_play_sound_click(self):
        print("SSSSSS")

class MainLayoutWidget(tkinter.Tk):
    object_cells = []

    def __init__(self, json_layout):
        tkinter.Tk.__init__(self)

        name = json_layout["name"]
        self.title(f"Layout: {name}")

        main_frame = ttk.Frame(
            self,
            width=int(self.winfo_screenwidth() / 2),
            height=int(self.winfo_screenheight() / 2),
        )
        main_frame.grid(row=0, column=0, sticky="nsew")

        rows = json_layout["layout"]["rows"]
        columns = json_layout["layout"]["columns"]

        cell_width = int(main_frame.winfo_reqwidth() / rows)
        cell_height = int(main_frame.winfo_reqheight() / columns)

        cells = json_layout["mapping"]["cells"]
        cells_column = [json.loads("{}") for c in range(0, columns)]
        cells_matrix = [list(cells_column) for r in range(0, rows)]

        for c in cells:
            cell_id = c["id"]
            row = int(cell_id / rows)
            column = int(cell_id % rows)
            cells_matrix[row][column] = c

        for r in range(0, rows):
            self.object_cells.append([])
            for c in range(0, columns):
                cell = cells_matrix[r][c]
                self.object_cells[r].append(
                    ObjectFrame(
                        main_frame,
                        (cell_width, cell_height),
                        cell["o"],
                        cell["i"],
                        cell["s"],
                    )
                )
                self.object_cells[r][c].grid(
                    row=r, column=c
                )  # , sticky ='w'+'n'+'e'+'s')


layout_name = "2.json"  # input("Please specify a layout name: ")
layout_json = layout_loader.load_layout_as_json(layout_name)

root = MainLayoutWidget(layout_json)
root.mainloop()

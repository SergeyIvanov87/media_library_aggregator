#!/usr/bin/python

import json
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk

import layout_loader


class ObjectRepresentative(tkinter.ttk.Button):
    images = []
    photo_images = []

    def __init__(self, parent, dimensions, description_list, images_list, sounds_list):
        self.images = [Image.open(pathToImage) for pathToImage in images_list]
        self.images = [img.resize(dimensions, Image.LANCZOS) for img in self.images]

        self.photo_images = [ImageTk.PhotoImage(image) for image in self.images]

        cur_image = self.__extract_next_photo_image__()
        tkinter.ttk.Button.__init__(
            self,
            parent,
            text=description_list[0],
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
                    ObjectRepresentative(
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

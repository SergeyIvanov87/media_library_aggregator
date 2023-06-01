#!/usr/bin/python
"""
The module asks for user input and creates a layout schema description (as JSON document)
which is used by the `layout_viewer.py` to represent objects (like pictures with sounds) in a
 grid-widget of a `rows x columns` dimension
"""

import json
import os
import shutil
import sys

import collector_utils
import layout_loader


# Input data
name = "2"  # input("Enter the layout name: ")
rows = int("2")  # int(input("Enter the layout dimensions[row]: "))
columns = int("2")  # int(input("Enter the layout dimensions[column]: "))

source_path = (
    # input("Enter path to objects: "),
    "/home/user/layout",
    # input("Enter path to pictures: "),
    "/home/user/layout",
    # input("Enter path to sounds: "),
    "/home/user/layout",
)

for path in source_path:
    if not os.path.isdir(path):
        sys.exit(f"ERROR: path: {path} must refer to directories")

new_layout_json = layout_loader.create_layout_contex_json(name, rows, columns)
new_layout_json["source"] = source_path

objects = collector_utils.process_objects(source_path[0])
print(f"Found objects:\n{objects}")

if len(objects) < rows * columns:
    sys.exit(
        f"To generate a proper layout schema you must set `row`: {rows} and `column`: {columns} values specifically\nin the way that its `product`: {rows * columns} would be less or equal to a number of founded objects: {len(objects)}.\nPlease try again.\n"
    )

objects_with_images = collector_utils.process_objects_attributes(
    source_path[1], collector_utils.is_image, objects
)
print(f"\nFound objects with images:\n{objects_with_images}")
objects_with_sounds = collector_utils.process_objects_attributes(
    source_path[2], collector_utils.is_sound, objects
)
print(f"\nFound objects with sounds:\n{objects_with_sounds}")
print("\n")

layout_loader.save_layout_as_json(new_layout_json, objects, objects_with_images, objects_with_sounds)

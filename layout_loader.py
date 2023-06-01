#!/usr/bin/python
"""
The module provides serialization & deserialization for a layout document format
JSON is only supported at the moment
"""

import json
import os
import random
import shutil


def create_layout_cell(cell_id, object_key, images_dict, sounds_dict):
    """
    Transform object and its attributes into JSON cell object
    """
    sounds_list = sounds_dict[object_key]
    images_list = images_dict[object_key]
    json_str = (
        "{"
        + f'"id": {cell_id}, "i": {images_list}, "o": ["{object_key}"], "s": {sounds_list}'
        + "}"
    )
    return json.loads(json_str.replace("'", '"'))

def load_layout_as_json(name):
    """
    open a file by name and load its content into JSON format
    """
    layout_filename = os.path.join("layouts", name)

    # Read file data
    try:
        layout_file = open(layout_filename, "r", encoding="utf-8")
    except OSError as err:
        sys.exit(
            f"Cannot open file JSON layout: {layout_filename}\nError: {err}"
        )
    with layout_file:
        try:
            json_data = json.load(layout_file)
        except Exception as err:
            sys.exit(
                f"Cannot parse JSON data a file: {layout_filename}\nError: {err}"
            )
    return json_data

def create_layout_contex_json(name, rows, columns):
    """
    Provides a special purpose object which describes JSON layout context.
    This context determines a handle object for saving JSON as a layout file
    """

    json_ctx = load_layout_as_json("layout_schema_json")
    json_ctx["name"] = name
    json_ctx["layout"]["rows"] = rows
    json_ctx["layout"]["columns"] = columns
    return json_ctx

def save_layout_as_json(json_ctx, objects, objects_with_images, objects_with_sounds):
    """
    Construct new layout from layout schema:
    Before doing that we shall copy the initial schema file
    and modify it according to entered parameters
    """
    name = json_ctx["name"]
    rows = json_ctx["layout"]["rows"]
    columns = json_ctx["layout"]["columns"]

    # remove stencil version of cell, which was just used for exposing a format representation
    if json_ctx["mapping"]["cells"][0]["id"] == 0:
        json_ctx["mapping"]["cells"].pop()

    # fill out cells using date from collected objects and its attributes by a random algorithm
    for r in range(0, rows):
        for c in range(0, columns):
            r_o = random.choice(objects)
            objects.remove(r_o)
            cell = create_layout_cell(
                str(r * columns + c), r_o, objects_with_images, objects_with_sounds
            )
            json_ctx["mapping"]["cells"].append(cell)

    # Save to file
    new_layout_filename = os.path.join("layouts", name + ".json")
    try:
        new_layout_file = open(new_layout_filename, "w", encoding="utf-8")
    except OSError as err:
        os.remove(new_layout_filename)
        sys.exit(
            f"Cannot open file for writing: {new_layout_filename}\nError: {err}"
        )
    with new_layout_file:
        json.dump(json_ctx, new_layout_file)

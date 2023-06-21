#!/usr/bin/python
"""
Module exports some auxiliary functions to read a file system and parse
objects (like text description files) and its attributes (sounds & images)
Attributes types may be expanded
"""

import os
import re


def is_file_with_extension(file_path, ext_set):
    if not os.path.isfile(file_path):
        return False

    return str.lower(os.path.splitext(file_path)[1]) in ext_set


def is_object(file_path):
    return is_file_with_extension(file_path, {".txt"})


def is_image(file_path):
    return is_file_with_extension(file_path, {".bmp", ".jpg", ".png"})


def is_sound(file_path):
    return is_file_with_extension(file_path, {".mp3", ".wav"})


def collect_file_list_match_condition(entry, match_condition):
    out_entries = []
    if match_condition(entry):
        return [entry]

    if os.path.isdir(entry):
        for f in os.listdir(entry):
            out_entries.extend(
                collect_file_list_match_condition(
                    os.path.join(entry, f), match_condition
                )
            )
    return out_entries


def process_objects(objects_path):
    """find all objects by path"""
    files_list = [
        os.path.join(objects_path, f)
        for f in os.listdir(objects_path)
        if os.path.isfile(os.path.join(objects_path, f))
    ]
    return [i for i in files_list if is_object(i)]

def file_name_to_object_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def process_objects_attributes(
    attributes_path, attribute_match_condition, objects_list
):
    """
    find attributes in each object-name directory under attributes_path
    or when file names matches regarding object name
    """
    object_attrfile_path = {}

    entry_list = [os.path.join(attributes_path, f) for f in os.listdir(attributes_path)]
    object_name = [file_name_to_object_name(o) for o in objects_list]
    # find attribute file path by regexp matching to an object_name pattern
    search_pattern = r"\.).*)|(.*(\/".join(object_name)
    search_pattern = r"(.*(\/" + search_pattern + "\.).*)"
    for e in entry_list:
        match = re.match(search_pattern, e)
        if not match:
            continue
        for g in match.groups():
            if not g:
                continue
            g_index = match.groups().index(g)
            if not g_index % 2:
                o = objects_list[int(g_index / 2)]
                # create key associated with object
                if o not in object_attrfile_path.keys():
                    object_attrfile_path[o] = []

                # add entry into o key
                object_attrfile_path[o].extend(
                    collect_file_list_match_condition(e, attribute_match_condition)
                )
    return object_attrfile_path

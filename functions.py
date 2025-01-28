import json
import os
import configparser
import bpy


def write_json(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_json(file):
    try:
        with open(file) as f:
            data = json.load(f)
            return data
    except:
        print(f"Error reading {file}")
        return None
    

def read_config(file):
    config = configparser.ConfigParser()
    try:
        config.read(file)
    except:
        print(f"Error reading {file}")
    return config

def write_config(config, file):
    with open(file, 'w') as configfile:
        config.write(configfile)


def get_addon_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_template(filename):
    return os.path.join(get_addon_dir(), 'templates', filename)


# default
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def open_folder(path):
    dir = path
    if os.path.isfile(path):
        dir = os.path.dirname(path)

    os.startfile(dir) # open folder


def get_properties(context):
    return context.scene.time_tracker_props


def get_blender_path(path):
    abs_path = bpy.path.abspath(path)
    if not os.path.exists(abs_path):
        return None
    return abs_path


import tomllib
def get_attr_from_manifest(attribute):
    # Verzeichnis des Add-ons ermitteln
    addon_dir = os.path.dirname(__file__)
    manifest_path = os.path.join(addon_dir, "blender_manifest.toml")
    
    if os.path.exists(manifest_path):
        with open(manifest_path, "rb") as f:  # Verwenden Sie "r" für `toml` statt `tomllib`
            manifest = tomllib.load(f)
            return manifest.get(attribute)  # ID aus der Datei holen
    return None

import datetime
def get_time_pretty(seconds: int) -> str:
    return str(datetime.timedelta(seconds=seconds))


"""
returns data_dir path
"""
def get_data_dir():
    return bpy.utils.extension_path_user(package=__package__, path="data", create=True)


from .properties import TIME_TRACK_FILE
def get_time_track_file():
    data_dir = get_data_dir()
    return os.path.join(data_dir, TIME_TRACK_FILE)


# TODO more functionality
# - save dates when worked on file (first, last or every date...)
# - hours/day
"""
persist_time_info()
    this method is responsible for converting and 
    saving the blend files time property to the disk
"""
def persist_time_info(tracking_file, time):
    data = {}
    if os.path.exists(tracking_file):
        data = read_json(tracking_file)
    
    blend_file = bpy.data.filepath
    if not blend_file:
        return False

    data[blend_file] = { "seconds": time, "time": get_time_pretty(seconds=time)}

    write_json(data, tracking_file)
    print(f"Saving time tracking data {data[blend_file]} in {tracking_file}")

    return True
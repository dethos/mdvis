from flask import Flask
import webbrowser
import os
import json

ALLOWED_IMAGE_EXTENSIONS = ["gif", "jpeg", "jpg", "bmp", "png"]

app = Flask(__name__)


# Initialization functions
def build_tree(rootDir='.'):
    for dirName, subdirList, fileList in os.walk(rootDir):
        dir_contents = get_dir_contents(fileList)
        path_nodes = dirName.split("/") if dirName != "." else []
        if path_nodes:
            own_node = path_nodes[-1]
            get_parent(path_nodes)[own_node] = dir_contents
        else:
            app.file_tree = dir_contents


def get_parent(path_nodes):
    current_parent = app.file_tree
    for parent in path_nodes[1:-1]:
        current_parent = current_parent[parent]
    return current_parent


def get_dir_contents(file_list):
    content = {}
    for fname in file_list:
        name_components = fname.split(".")
        extension = name_components[-1] if len(name_components) > 1 else None
        content[fname] = {"extension": extension}
    return content


def run_server(open_browser=True):
    if open_browser:
        browser = webbrowser.get()
        browser.open("http://localhost:5000")
    app.run()


# Flask Routes, executed per request
@app.route("/")
def index():
    return "Hello World!"


@app.route("/<path:file>")
def show(file):
    return "true"


# Entry points
def execute():
    """Function to be called from the commandline"""
    build_tree()
    run_server()

from flask import Flask, send_file, render_template, redirect, url_for, request
from markdown import markdown as md
from random import randint
from jinja2 import Markup
import webbrowser
import os
import logging
import sys


ALLOWED_EXTENSIONS = ["gif", "jpeg", "jpg", "bmp", "png", "mp4", "webm"]
INDEX_PAGES = ["index", "readme"]

app = Flask(__name__)


# Initialization functions
# The below 3 function need to be refactored
def build_tree(root_dir='.', depth=4):
    """
    Searches the current folder for directories and files, up to
    n (4 default) levels deep and stores the structure.
    This stricture is used later, when the server is running.
    """
    for dir_name, subdir_list, file_list in os.walk(root_dir):
        path_nodes = dir_name.split("/") if dir_name != "." else []
        if len(path_nodes) > depth:
            continue
        dir_contents = get_dir_contents(file_list)
        if path_nodes:
            if dir_contents:
                own_node = path_nodes[-1]
                get_parent(path_nodes)[own_node] = dir_contents
        else:
            app.file_tree = dir_contents


def get_parent(path_nodes):
    current_parent = app.file_tree
    for parent in path_nodes[1:-1]:
        if parent not in current_parent:
            current_parent[parent] = {}
        current_parent = current_parent[parent]
    return current_parent


def get_dir_contents(file_list):
    content = {}
    for fname in file_list:
        # Get name components
        n_sections = fname.split(".")
        # Only for index check
        name = n_sections[0].lower()
        extension = n_sections[-1].lower() if len(n_sections) > 1 else None
        index = False
        if extension == "md" or extension in ALLOWED_EXTENSIONS:
            if name in INDEX_PAGES and extension not in ALLOWED_EXTENSIONS:
                index = True
            content[fname] = {"extension": extension, 'is_index': index}
    return content


def run_server(open_browser=True):
    """
    Simply starts the http server that the provide the contents
    of the md files
    """
    port = randint(2000, 65000)
    if open_browser:
        browser = webbrowser.get()
        browser.open("http://localhost:{}".format(port))
    app.run(port=port, use_reloader=False, debug=True)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# Helpers
def get_index_file(obj):
    for name in obj:
        if obj[name].get("is_index", ''):
            return name
    return ""


def get_html_version(file_path):
    with open("./{}".format(file_path)) as f:
        html = Markup(md(f.read(), extensions=['gfm']))
    return html


def generate_menu(node, path=""):
    domlist = "<ul>{}</ul>"
    elements = []
    if node.get("extension", ''):
        return ''
    for key in sorted(node.keys()):
        element = "<li>{}</li>"
        subdir = generate_menu(node[key], "{}/{}".format(path, key))
        content = "<a href='{}/{}' target='content-frame'>{}</a><br>{}"
        content = content.format(path, key, key, subdir)
        elements.append(element.format(content))

    return domlist.format("".join(elements))


# Flask Routes, executed per request
@app.route("/")
def index():
    """ Servers the page the the wieframes / iframes"""
    menu = Markup(generate_menu(app.file_tree))
    indexpage = get_index_file(app.file_tree)
    return render_template("index.html",
                           indexpage=indexpage,
                           menu=menu)


@app.route("/<path:file_path>", methods=["GET"])
def show(file_path):
    """ Servers the html version of the files if they exist"""
    path_elements = file_path.split("/")
    node = app.file_tree
    for elem in path_elements:
        node = node.get(elem, {})
    if node:
        if node.get("extension", "") in ALLOWED_EXTENSIONS:
            return send_file("{}/{}".format(os.getcwd(), file_path))
        # Still need to add the case where it is not an allowed file type
        elif node.get("extension", "") == "md":
            content = get_html_version(file_path)
            return render_template("document.html",
                                   content=content,
                                   file_path=file_path)
        else:
            ifile = get_index_file(node)
            if ifile:
                return redirect(url_for("show",
                                        file_path="{}/{}".format(file_path,
                                                                 ifile)))

    return "Markdown file not found."


@app.route("/close", methods=["POST"])
def close():
    shutdown_server()
    return "Shutting Down ..."


@app.before_first_request
def setup_logging():
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.CRITICAL)


# Entry points
def execute():
    """Function to be called from the commandline"""
    build_tree()
    run_server()


if __name__ == '__main__':
    # Used for easily running in development
    execute()

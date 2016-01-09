from flask import Flask
import webbrowser

app = Flask(__name__)
app.file_tree = {}


# Initialization functions
def build_tree():
    pass


def run_server(open_browser=False):
    if open_browser:
        browser = webbrowser.get()
        browser.open("http://localhost:5000")
    app.run()


# Flask Routes, executed per request
@app.route("/")
def index():
    return "Hello World!"


@app.route("/:file:")
def show(file):
    return "page"


# Entry points
def execute():
    """Function to be called from the commandline"""
    build_tree()
    run_server()

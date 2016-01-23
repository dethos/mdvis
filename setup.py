from setuptools import setup

long_description = """This simple program launches the browser and serves all
Mardown files in a given folder formated as beautiful html pages for easy
reading and navigation.
"""

setup(
    name="mdvis",
    version="0.1.0",
    author="Gonçalo Valério",
    author_email="gon@ovalerio.net",
    url="https://github.com/dethos/mdvis",
    description="Simple way to read folders of mardown files on the browser",
    long_description=long_description,
    license="GPLv3",
    classifiers=[
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Text Processing :: Markup",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    packages=["mdvis"],
    install_requires=[
        "flask>=0.10.1",
        "markdown>=2.6.5"
    ],
    entry_points={
        'console_scripts': [
            'mdvis = mdvis.server:execute',
        ]
    }
)

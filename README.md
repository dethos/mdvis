mdvis
=====

A quick and dirty way to visualize folders containing lot of markdown files. 

Often I need to check lots of markdown documents stored, for example, in git repositories. Opening and reading those files in a text editor, while an easy task, is not a pleasant reading experience. Navigating through the files on _Github_ can be a pain.

I sketched this little program, so you can quickly go through all the `.md` files contained in a folder (and its sub-folders) in the browser as if you were seeing them on _Github_ (even off-line).


## Install

This package is destined only to python 3 users.

If you use `pip` just run the following command:

> $ pip install mdvis

on many operating systems python 3 is not the default version in this case the command should be:

> pip3 install mdvis

Without resorting to `pip` to install you will need to clone the repository and run:

> $ python setup.py install

**Note:** On some systems you might need to use `sudo`

## Usage

Go to a given folder and type on the terminal:

> $ mdvis

This should launch a new tab in your browser


## Contributing

If this program is useful to you, you can help make it better. Open any issues you find or if you could provide fixes and new features creating new pull requests.

The design also needs improvements so new `css` and `html` changes are welcome.

## Acknowledgments

The current css used on the generated pages was taken from the following project:

* [Markdown Styles](https://github.com/mixu/markdown-styles)

All the credits should go its contributors

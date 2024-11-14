# TP 4

## Project description
The link to the deployed project is [here](https://pypi.org/project/easy-git-cli/)
The link to the repository is [here](https://github.com/OmarAllouch/devtools-easy-git/)
The tool I created is a command line tool that makes it easier to use git commands.
It is called `easy-git-cli`, and it's a python package that can be installed using pip.
For now it only supports a single command, which is `easy-git quick-commit` or `easy-git c` for short, which helps you stage files, commit them, and push them if you wish to, all in a single command and easy to use interface.


## Build tool
The build tool I used is `poetry`, which is a python package manager and build tool.
I used it to:
- Manage dependencies
- Manage project versions
- Package the project into a wheel file
- Build the project
- Publish the project to pypi

## Build instructions
The README file provides clear documentation on how to install and run the tool.
However, it doesn't include the build instructions as it's not meant to be used in that way.

If you wish to build the project, you can follow these steps:
- Clone the repository
- Install poetry using `pip install poetry`
- Run `poetry install` to install the dependencies
- Run `poetry run python src/main.py quick-commit (or c)` to run the tool.

## Build tool configuration
The build tool configuration file is `pyproject.toml`, which is the configuration file for poetry.
It includes the project metadata, dependencies, and build configuration.

## Quick access
I made a `Makefile` that includes a command for installing and running the tool.
You can run `make` to install it, and `make run` to run it (runs the help, just to ensure the tool is installed).

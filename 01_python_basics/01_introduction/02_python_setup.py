# this file explains python setup and environment basics

# python versions
# python comes in two major versions: python 2 and python 3
# we use python 3 as python 2 is no longer supported

# checking python version
import sys
print("python version:", sys.version)
print("version info:", sys.version_info)

# python installation
# windows: download from python.org
# mac: comes pre-installed or use homebrew
# linux: usually pre-installed or use package manager

# running python
# 1. interactive mode (REPL - Read, Eval, Print, Loop)
# python
# >>> print("hello")
# >>> 2 + 2
# >>> exit()

# 2. running scripts
# python script.py

# 3. IDE (integrated development environment)
# popular IDEs:
# - vscode
# - pycharm
# - jupyter notebook

# python environment
# showing current working directory
import os
print("\ncurrent working directory:", os.getcwd())

# showing environment variables
print("\npython path:", os.getenv("PYTHONPATH"))

# virtual environments
# used to isolate project dependencies
# creating: python -m venv myenv
# activating:
# - windows: myenv\Scripts\activate
# - unix: source myenv/bin/activate

# package management
# pip - python package installer
# common commands:
# pip install package_name
# pip uninstall package_name
# pip list
# pip freeze > requirements.txt

# importing modules
# standard library modules
import math
print("\npi value:", math.pi)

# third-party modules (need to be installed first)
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# python path
print("\npython search path:")
for path in sys.path:
    print(path)

# practice exercises:
# 1. create a virtual environment and:
#    - activate it
#    - install a package
#    - list installed packages
#    - deactivate it

# 2. write a script that:
#    - prints python version
#    - prints operating system
#    - prints environment variables
#    - prints current directory

# 3. create a requirements.txt file:
#    - install several packages
#    - freeze requirements
#    - create new environment
#    - install from requirements.txt

# example solution for #2:
import platform

print("\nsystem information:")
print("python version:", sys.version.split()[0])
print("operating system:", platform.system())
print("current directory:", os.getcwd())
print("number of cpu cores:", os.cpu_count()) 
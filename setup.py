import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['themes/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI"
)

# SETUP CX FREEZE
setup(
    name = "ExploreCity",
    author = "Hiba Elouazi",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    
)
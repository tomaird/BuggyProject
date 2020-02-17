import sys
from cx_Freeze import setup, Executable
import os


#os.environ['TCL_LIBRARY'] = r'C:\Users\group1\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
#os.environ['TK_LIBRARY'] = r'C:\Users\group1\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

build_exe_options = {"packages": ["os","tkinter","lxml","bs4","urllib","serial","time"]}

setup(name = "buggyMain_v3" ,
      version = "0.1" ,
      description = "" ,
      options = {"build_exe": build_exe_options},
      executables = [Executable("buggyMain_v3.py", base="Win32GUI")])

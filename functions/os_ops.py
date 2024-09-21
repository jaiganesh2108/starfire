import os
import subprocess as sp

paths = {
    'notepad': "C:\\Windows\\System32\\notepad.exe",
    'discord': "C:\\Users\\ashut\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'msedge':"C:\\Users\\jaig7\\OneDrive\\Desktop\\msedg.exe",
    'mspaint':"C:\\Users\\jaig7\\OneDrive\\Desktop\\mspaint.exe",
    }


def open_notepad():
    os.startfile(paths['notepad'])

def open_discord():
    os.startfile(paths['discord'])

def open_cmd():
    os.system('start cmd')

def open_edge():
    os.startfile("msedge")  # Windows command to open Microsoft Edge

def open_paint():
    os.startfile("mspaint")  # Windows command to open Microsoft Paint

def open_file_explorer():
    os.startfile(r'C:\Users\jaig7')

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def open_calculator():
    sp.Popen(paths['calculator'])


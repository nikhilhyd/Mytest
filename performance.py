import os
import time
import subprocess
from Tkinter import *
from functools import partial
from PIL import Image, ImageTk
from collections import defaultdict

# Dictionary of Test Script files and executables
scripts = defaultdict(lambda: defaultdict(dict))
scripts['furmark']['wfile'] = "start_furmark_windowed_1024x640.sh"
scripts['furmark']['ffile'] = "start_furmark_benchmark_fullscreen_1920x1080.sh"
scripts['tessmark']['wfile'] = "start_tessmark_windowed_1024x640.sh"
scripts['tessmark']['ffile'] = "start_tessmark_benchmark_fullscreen_1920x1080.sh"
scripts['piano']['wfile'] = "start_pixmark_piano_windowed_1024x640.sh"
scripts['piano']['ffile'] = "start_pixmark_piano_benchmark_fullscreen_1920x1080.sh"
scripts['gimark']['wfile'] = "start_gimark_windowed_1024x640.sh"
scripts['gimark']['ffile'] = "start_gimark_benchmark_fullscreen_1920x1080.sh"
scripts['vol']['wfile'] = "start_pixmark_volplosion_windowed_1024x640.sh"
scripts['vol']['ffile'] = "start_pixmark_volplosion_benchmark_fullscreen_1920x1080.sh"
scripts['triangle']['wfile'] = "start_triangle_windowed_1024x640.sh"
scripts['triangle']['ffile'] = "start_triangle_benchmark_fullscreen_1920x1080.sh"
scripts['plot3d']['wfile'] = "start_plot3d_windowed_1024x640.sh"
scripts['plot3d']['ffile'] = "start_plot3d_benchmark_fullscreen_1920x1080.sh"
scripts['windows']['glx'] = "wglgears.exe"
scripts['windows']['furmark'] = "FurMark.exe"
scripts['windows']['tessmark'] = "TessMark.exe"

# Dictionary of Test Case Names
tname = defaultdict(lambda: defaultdict(dict))
tname['wm']['file'] = "wfile"
tname['fm']['file'] = "ffile"
tname['wm']['Name'] = "window mode"
tname['fm']['Name'] = "full mode"
tname['glx']['Name'] = "Glx Gears"
tname['furmark']['Name'] = "FurMark Stress Test"
tname['tessmark']['Name'] = "TessMark Tessellation Test"
tname['gimark']['Name'] = "GiMark geometry instancing Test"
tname['piano']['Name'] = "Piano pixel shader Test"
tname['vol']['Name'] = "Volplosion pixel shader Test"
tname['triangle']['Name'] = "Triangle 3D Scene"
tname['plot3d']['Name'] = "Plot3D vertex shader Test"


root = Tk()
root.title("AMD GPU")
root.geometry('647x370+0+0')
root.configure(background='violet')
root.resizable(FALSE,FALSE)

f1 = Frame(root, bg="violet")
f2 = Frame(root, bg="violet")
f3 = Frame(root, bg="violet")

for frame in (f1, f2, f3):
    frame.grid(row=0, column=0, sticky='news')

def raise_frame(frame, option):
    global f3
    frame.tkraise()
    tname['set'] = option
    if option == "sysinfo":
        SystemInfo()


n = 4
path = "image/radeon.png"
img1 = Image.open(path)
[imageSizeWidth, imageSizeHeight] = img1.size
newImageSizeWidth = int(imageSizeWidth)
newImageSizeHeight = int(imageSizeHeight/n)

img1 = img1.resize((newImageSizeWidth, newImageSizeHeight))
img = ImageTk.PhotoImage(img1)
panel1 = Label(f1, image=img).pack(side="top")
panel2 = Label(f2, image=img).pack(side="top")


def lnxapplication(string):
    cwd = os.getcwd()
    mode = tname['set']
    filetype = tname[mode]['file']
    filename = scripts[string][filetype]
    path = cwd+"/lnxscripts/"
    os.chdir(path)
    cmd = "sh"+" "+filename
    print cmd
    os.system(cmd)
    os.chdir(cwd)


def radeontopcmd(command):
    cmd = "sudo"+" "+command
    cmd = "sudo"+" "+"gnome-terminal"+" "+"-e"+" "+"\"bash"+" "+"-c"+" "+"radeontop;bash"+"\""
    print cmd
    os.system(cmd)


def winapplication(string):
    application = scripts['windows'][string]
    os.system(application)


def SystemInfo():
    cmd = "cat /proc/cpuinfo | grep \"model name\" | awk NR==1 | cut -d : -f 2 | sed \"s/^ //g\""
    processor_name = subprocess.check_output(cmd, shell=True)
    cmd = "cat /proc/cpuinfo | grep \"cpu cores\" | awk NR==1 | cut -d : -f 2 | sed \"s/ //g\""
    cpu_cores = subprocess.check_output(cmd, shell=True)
    cmd = "cat /proc/cpuinfo | grep \"cpu MHz\" | awk NR==1 | cut -d : -f 2 | sed \"s/ //g\""
    cpu_mhz = subprocess.check_output(cmd, shell=True)
    cmd = "cat /proc/meminfo | grep MemTotal | awk NR==1 | cut -d : -f 2 | sed \"s/^[ \t]*//g\""
    total_mem = subprocess.check_output(cmd, shell=True)
    cmd = "cat /proc/meminfo | grep MemFree | awk NR==1 | cut -d : -f 2 | sed \"s/^[ \t]*//g\""
    free_mem = subprocess.check_output(cmd, shell=True)
    cmd = "cat /proc/meminfo | grep MemAvailable | awk NR==1 | cut -d : -f 2 | sed \"s/^[ \t]*//g\""
    available_mem = subprocess.check_output(cmd, shell=True)
    l4 = Label(f3, text=processor_name, bg="violet", anchor=CENTER).pack()
    l5 = Label(f3, text=cpu_mhz, bg="violet", anchor=CENTER).pack()
    l6 = Label(f3, text=cpu_cores, bg="violet", anchor=CENTER).pack()
    l7 = Label(f3, text=total_mem, bg="violet", anchor=CENTER).pack()
    l8 = Label(f3, text=free_mem, bg="violet", anchor=CENTER).pack()
    l9 = Label(f3, text=available_mem, bg="violet", anchor=CENTER).pack()
    Button(f3, text='Return to Main Menu', command=lambda:raise_frame(f1, "sysinforeturn"), bg="yellow", relief=RAISED).pack(padx=1, pady=1)

# Main Menu
L1 = Label(f1, text="LINUX APPLICATIONS", bg="violet").pack(padx=1, pady=1)
L2 = Label(f2, text="Test Cases", bg="violet").pack(padx=1, pady=1)
for item in ("wm", "fm"):
    BName = tname[item]['Name']
    Button(f1, text=str(BName), command=lambda item=item: raise_frame(f2,item), bg="yellow", relief=RAISED).pack(padx=1, pady=1)

sysinfo = "System Information"
Button(f1, text=sysinfo, command=lambda sysinfo=sysinfo: raise_frame(f3,"sysinfo"), bg="yellow", relief=RAISED).pack(padx=1, pady=1)
name = "radeontop"
Button(f1, text="radeontop", command=lambda name=name: radeontopcmd("radeontop"), bg="yellow", relief=RAISED).pack(padx=1, pady=1)

# Sub Menu
for item1 in ("furmark", "piano", "vol", "plot3d", "triangle", "tessmark", "gimark"):
    Name = tname[item1]['Name']
    Button(f2, text=str(Name), command=lambda item1=item1: lnxapplication(item1), bg="yellow", relief=RAISED).pack(padx=1, pady=1)
Button(f2, text='Return to Main Menu', command=lambda:raise_frame(f1, "ss"), bg="yellow", relief=RAISED).pack(padx=1, pady=1)

'''
TODO ADD HERE WINDOWS BASED APPLICATIONS
L3 = Label(f1, text="WINDOWS APPLICATIONS", bg="violet").pack(padx=1, pady=1)
for testname in ("glx", "furmark", "tessmark"):
    Name = tname[testname]['Name']
    Button(f1, text=str(Name), command=lambda testname=testname: winapplication(testname), bg="yellow", relief=RAISED).pack(padx=1, pady=1)
'''

raise_frame(f1, "ss")
if "nt" == os.name:
    root.wm_iconbitmap(bitmap="image/amd.ico")
else:
    root.wm_iconbitmap(bitmap="@image/amd.xbm")
root.mainloop()


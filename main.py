from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog, PhotoImage
from app import gui_mode

def get_icon_image():
    # Load the icon image
    icon_path = "icon.png"
    image = Image.open(icon_path)
    return image

def show_gui(icon, item):
    icon.stop()
    gui_mode()

def exit_app(icon, item):
    icon.stop()
    exit(1)

# System Tray Icon
icon = pystray.Icon("video_converter", get_icon_image(), "Video Converter", 
    menu=pystray.Menu(
        item('Open Video Resizer', show_gui),
        item('Exit', exit_app)
    ))

icon.run()

import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import argparse
from threading import Thread

running_process = None


def convert_video(input_file, output_file, resolution, crf_value, audio_option, sample_rate, bit_depth):
    
    ffmpeg_path = 'ffmpeg'
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    command = [
        ffmpeg_path,
        '-y',  # Overwrite existing files without asking
        '-hwaccel', 'cuda',
        '-hwaccel_output_format', 'cuda',
        '-i', input_file
    ]
    
    # Add audio options
    if audio_option == "Copy Audio":
        command.extend(['-c:a', 'copy'])
    else:
        command.extend([
            '-c:a', 'aac',
            '-b:a', '512k',  # High bitrate for fixed bitrate encoding, you can increase this if needed
            '-ar', f'{sample_rate}',  # Set audio sample rate to 48kHz
    ])

    # Add resolution-specific options
    if resolution == "4K":
        command.extend([
            '-vf', 'scale=3840:-1',
            '-c:v', 'hevc_nvenc',
            '-preset', 'p7',
            '-profile:v', 'main10',
            '-rc', 'vbr',  # Use high-quality VBR mode
            '-strict', '-2',
            '-cq:v', crf_value,
            '-b:v', '25M',
            '-maxrate:v', '30M',
            '-bufsize:v', '30M',
            '-pix_fmt', 'yuv420p10le'
        ])
    elif resolution == "8K":
        command.extend([
            '-vf', 'scale=7680:-1',
            '-c:v', 'hevc_nvenc',
            '-preset', 'p7',  # Use 'p7' for 10-bit, 'slow' is not a valid preset for NVENC
            '-profile:v', 'main10',  # Set profile to main10 for 10-bit encoding
            '-rc', 'vbr',  # Use high-quality VBR mode
            '-strict', '-2',
            '-cq:v', crf_value,  # Set the constant quality level for VBR
            '-b:v', '25M',
            '-maxrate:v', '30M',
            '-bufsize:v', '30M',
            '-pix_fmt', 'yuv420p10le'  # Ensure 10-bit pixel format
    ])
    
    command.append(output_file)
    
    # Execute the command and return the subprocess
    global running_process
    running_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    return running_process

def stop_conversion():
    global running_process
    if running_process:
        running_process.terminate()  # Sends SIGTERM to the process
        running_process = None
        
def update_console(process, console):
    for line in iter(process.stdout.readline, ''):  # Read the output line by line until it's empty
        console.insert(tk.END, line)
        console.see(tk.END)
    process.stdout.close()
    process.wait()
    console.insert(tk.END, "Conversion Completed!\n")

def gui_mode():
    def open_file_dialog():
        input_file = filedialog.askopenfilename(title="Select a Video File", filetypes=[("Video files", "*.mp4 *.mov *.avi"), ("All files", "*.*")])
        if input_file:
            output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
            if output_file:
                process = convert_video(
                    input_file, output_file, resolution_var.get(),
                    quality_var.get(), audio_option_var.get(),
                    sample_rate_var.get(), bit_depth_var.get()
                )
                Thread(target=update_console, args=(process, console), daemon=True).start()

    root = tk.Tk()
    root.title("Video Resizer Tool for Topaz Video Ai (post-script)")
    root.configure(bg='#2e2e2e')
    root.geometry("600x400")  # Adjust the size of the window as needed

    # Define Variables
    quality_var = tk.StringVar(value="15")
    audio_option_var = tk.StringVar(value="Copy Audio")
    resolution_var = tk.StringVar(value="4K")
    sample_rate_var = tk.StringVar(value="48000")
    bit_depth_var = tk.StringVar(value="24")

    # Create Drop-down Menus
    quality_menu = tk.OptionMenu(root, quality_var, "15", "18", "20", "23", "25")
    quality_menu.pack()

    audio_option_menu = tk.OptionMenu(root, audio_option_var, "Copy Audio", "Reencode Audio")
    audio_option_menu.pack()

    resolution_menu = tk.OptionMenu(root, resolution_var, "4K", "8K")
    resolution_menu.pack()

    sample_rate_menu = tk.OptionMenu(root, sample_rate_var, "44100", "48000", "96000")
    sample_rate_menu.pack()

    bit_depth_menu = tk.OptionMenu(root, bit_depth_var, "16", "24", "32")
    bit_depth_menu.pack()

    # Buttons
    button_style = {'bg': '#4c4c4c', 'fg': '#ffffff', 'padx': 10, 'pady': 5, 'font': ('Arial', 12, 'bold')}
    select_button = tk.Button(root, text="Select Video", command=open_file_dialog, **button_style)
    select_button.pack()

    # # Stop Button
    # stop_button = tk.Button(root, text="Stop Conversion", command=stop_conversion, **button_style)
    # stop_button.pack()
    
    # Console Output
    console = scrolledtext.ScrolledText(root, height=40, bg="#2e2e2e", fg="#ffffff")
    console.pack()

    root.mainloop()

def cli_mode(args):
    result = convert_video(args.input_file, args.output_file, args.resolution, args.crf_value, args.audio_option, args.sample_rate, args.bit_depth)
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert videos to MP4 format.", argument_default="--help")
    parser.add_argument("--input", help="Input video file path.")
    parser.add_argument("--output", help="Output video file path.")
    parser.add_argument("--quality", help="Quality level (CRF value)", default="15")
    parser.add_argument("--audio", help="Audio format (stereo or binaural)", default="stereo")
    parser.add_argument("--resolution", help="Video resolution (4K or 8K)", default="8K")
    parser.add_argument("--sample_rate", help="Audio sample rate", default="48000")
    parser.add_argument("--bit_depth", help="Audio bit depth", default="24")
    parser.add_argument("--gui", help="Launch GUI mode", action="store_true")

    args = parser.parse_args()

    if args.gui:
        gui_mode()
    else:
        cli_mode(args)

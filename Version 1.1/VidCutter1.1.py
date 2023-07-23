import time
import tkinter as tk
import tkinter.messagebox as messagebox
import webbrowser
from datetime import datetime
from tkinter import filedialog
import threading
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def select_input_file():
    input_file = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=(("Video Files", "*.mp4 *.avi *.mkv"), ("All Files", "*.*")),
    )
    if input_file:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, input_file)


def select_output_file():
    output_file = filedialog.asksaveasfilename(
        title="Save Cut Video As",
        defaultextension=".mp4",
        filetypes=(("Video Files", "*.mp4 *.avi *.mkv"), ("All Files", "*.*")),
    )
    if output_file:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_file)


def time_to_seconds(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
    seconds = (time_obj - datetime(1900, 1, 1)).total_seconds()
    return seconds


def update_status_label():
    for _ in range(10):  # Number of times to blink
        status_label.config(
            text="Cutting video in progress", fg="#CC1512", bg="#FFFFFF"
        )
        window.update()
        time.sleep(0.5)
        status_label.config(
            text="Cutting video in progress", fg="#FBFFFF", bg="#CC1512"
        )
        window.update()
        time.sleep(0.5)


def cut_video():
    def perform_cut():
        input_file = input_entry.get()
        start_time = entry_start.get()
        end_time = entry_end.get()
        output_file = output_entry.get()

        try:
            start_seconds = time_to_seconds(start_time)
            end_seconds = time_to_seconds(end_time)

            threading.Thread(target=update_status_label).start()

            ffmpeg_extract_subclip(
                input_file, start_seconds, end_seconds, targetname=output_file
            )

            # Update the status label after the cutting is completed
            # Blink the status label text
            for _ in range(10):  # Number of times to blink
                status_label.config(
                    text="Video cut successfully!", fg="#000000", bg="#FFFFFF"
                )
                window.update()
                time.sleep(0.5)
                status_label.config(
                    text="Video cut successfully!", fg="#FBFFFF", bg="#000000"
                )
                window.update()
                time.sleep(0.5)
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")

    threading.Thread(target=perform_cut).start()


def preview_video():
    def perform_preview():
        input_file = input_entry.get()
        start_time = entry_start.get()
        end_time = entry_end.get()

        try:
            start_seconds = time_to_seconds(start_time)
            end_seconds = time_to_seconds(end_time)

            clip = VideoFileClip(input_file)
            clip = clip.subclip(start_seconds, end_seconds)
            clip.preview()
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")

    threading.Thread(target=perform_preview).start()


def exit_application():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        window.destroy()


def show_help():
    messagebox.showinfo(
        "How to use",
        "1. Select an input video file\n2. Choose an output file name and location\n3. Specify the start and end time for the video segment\n4. Click 'Cut Video' to extract and save the specified segment\n\nNote: Alternatively, click 'Preview Cut' to preview the segment without saving",
    )


def show_about():
    messagebox.showinfo("About", "Video Cutter\nVersion 1.1\n\nCreated by pudszTTIOT")


def open_help_file():
    # Replace with the actual path to your help file
    help_file_path = (
        "G:\Software\py\Python Creations\Completed\Projects\VidCutter\Docs\Readme.txt"
    )
    webbrowser.open(help_file_path)


def check_version():
    messagebox.showinfo("Version", "Video Cutter\nVersion 1.1")


def toggle_theme():
    current_bg = window.cget("bg")

    if current_bg == "#3CB371":  # If current theme is light theme
        # Switch to dark theme
        window.configure(bg="#2A292B")
        heading_label.configure(bg="#fff694", fg="#2a292b")
        input_entry.configure(bg="#fbfdfd", fg="#353535")
        output_entry.configure(bg="#fbfdfd", fg="#353535")
        entry_start.configure(bg="#fff694", fg="#353535")
        entry_end.configure(bg="#fff694", fg="#353535")
        status_label.configure(bg="#CC1512", fg="#FBFFFF")
        watermark_label.configure(bg="#2A292B", fg="#46F953")
        cut_button.configure(bg="#2c7ce6", fg="#d6a160")
        preview_button.configure(bg="#ff8ffd", fg="#333333")
        theme_button.configure(bg="#041928", fg="#FFCB05")
    else:
        # Switch to light theme
        window.configure(bg="#3CB371")
        heading_label.configure(bg="#2A292B", fg="#FFF01F")
        input_entry.configure(bg="#F7FCFC", fg="#000000")
        output_entry.configure(bg="#F7FCFC", fg="#000000")
        entry_start.configure(bg="#2A292B", fg="#FFFFFF")
        entry_end.configure(bg="#2A292B", fg="#FFFFFF")
        status_label.configure(bg="#CC1512", fg="#FBFFFF")
        watermark_label.configure(bg="#2A292B", fg="#46F953")
        cut_button.configure(bg="#B33C7E", fg="#FBFFFF")
        preview_button.configure(bg="#713CB3", fg="#FBFFFF")
        theme_button.configure(bg="#FFCB05", fg="#20211A")


# Create the GUI
window = tk.Tk()
window.title("VidCutter")
window.iconbitmap(
    r"G:\Software\py\Python Creations\Completed\Projects\VidCutter\Images\video cut.ico"
)  # Set the path to your icon file

# Menu bar
menubar = tk.Menu(window)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=exit_application)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="How to use", command=show_help)
help_menu.add_command(label="Help File", command=open_help_file)
help_menu.add_separator()
help_menu.add_command(label="About...", command=show_about)
menubar.add_cascade(label="Help", menu=help_menu)

version_menu = tk.Menu(menubar, tearoff=0)
version_menu.add_command(label="Check Version", command=check_version)
menubar.add_cascade(label="Version", menu=version_menu)

window.config(menu=menubar)

# Heading title at top
heading_label = tk.Label(
    window, text="VidCutter", font=("THE BOLD FONT", 25), bg="#2A292B", fg="#FFF01F"
)
heading_label.pack(pady=(8, 0))

# Input file selection
input_button = tk.Button(
    window,
    text="Select Input File",
    font=("Tahoma", 12),
    bg="#E7E9EA",
    fg="#20211A",
    command=select_input_file,
)
input_button.pack(fill="both", expand=True, pady=(10, 0))
input_entry = tk.Entry(window, bg="#F7FCFC")
input_entry.pack(fill="both", expand=True, pady=(0, 5))

# Output file selection
output_button = tk.Button(
    window,
    text="Select Output File",
    font=("Tahoma", 12),
    bg="#E7E9EA",
    fg="#20211A",
    command=select_output_file,
)
output_button.pack(fill="both", expand=True, pady=(5, 0))
output_entry = tk.Entry(window, bg="#F7FCFC")
output_entry.pack(fill="both", expand=True, pady=(0, 5))


# Start time input
label_start = tk.Label(
    window,
    text="Start Time (hh:mm:ss.mmm)",
    font=("Tahoma", 12),
    bg="#E7E9EA",
    fg="#20211A",
)
label_start.pack(pady=(5, 1))
entry_start = tk.Entry(
    window, justify="center", font=("Tahoma", 12), bg="#2A292B", fg="#FFFFFF"
)
entry_start.insert(0, "00:00:00.000")
entry_start.pack(pady=(0, 5))

# End time input
label_end = tk.Label(
    window,
    text="End Time (hh:mm:ss.mmm)",
    font=("Tahoma", 12),
    bg="#E7E9EA",
    fg="#20211A",
)
label_end.pack(pady=(5, 1))
entry_end = tk.Entry(
    window, justify="center", font=("Tahoma", 12), bg="#2A292B", fg="#FFFFFF"
)
entry_end.insert(0, "00:00:00.000")
entry_end.pack(pady=(0, 5))

# Cut button
cut_button = tk.Button(
    window,
    text="Cut Video",
    font=("THE BOLD FONT", 14),
    bg="#B33C7E",
    fg="#FBFFFF",
    command=cut_video,
)
cut_button.pack(pady=(5, 0))

# Preview button
preview_button = tk.Button(
    window,
    text="Preview Cut",
    font=("THE BOLD FONT", 14),
    bg="#713CB3",
    fg="#FBFFFF",
    command=preview_video,
)
preview_button.pack(pady=(5, 0))

# Status label
status_label = tk.Label(window, text="")
status_label.pack(pady=(5, 0))

# Toggle theme button
theme_button = tk.Button(
    window,
    text="Toggle Theme",
    font=("Closeness Regular", 16),
    bg="#FFCB05",
    fg="#20211A",
    command=toggle_theme,
)
theme_button.pack(pady=(5, 6))

# Watermark label
watermark_label = tk.Label(
    window, text="pudszTTIOT", font=("Corbel", 9), bg="#2A292B", fg="#46F953"
)
watermark_label.place(relx=1.0, rely=1.0, anchor="se", x=0, y=0)

window.configure(bg="#3CB371")
window.geometry("485x485")
window.mainloop()

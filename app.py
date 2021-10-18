import tkinter as tk
from tkinter import ttk, filedialog as fd
import pytube
import os
from PIL import Image, ImageTk


# On button click
def convert():
    try:
        f = fd.asksaveasfilename(defaultextension=".mp4")
        print(f)

        if f is None:
            return
        elif format_combobox.get() == "MP4":
            downloadmp4(f)
        elif format_combobox.get() == "MP3":
            downloadmp3(f)

    except Exception as e:
        print(e)
        notif.config(fg="#ff1c1c")
        notif_text.set("Invalid path")
        print("Invalid path selected")


def downloadmp4(directory):
    file_name = directory.split("/")[-1]
    direc = "/".join(directory.split("/")[:-1])
    video_url = url.get()

    try:
        youtube = pytube.YouTube(video_url)
        notif.config(fg="black")
        notif_text.set(f"Downloading \"{youtube.title}\"...")

        video = youtube.streams.filter(
            progressive=True, file_extension="mp4").get_highest_resolution()
        video.download(direc, filename=file_name.split(".")[0] + ".mp4")

        notif.config(fg="green")
        notif_text.set("Video downloaded successfully")

    except Exception as e:
        print(e)
        notif.config(fg="#ff1c1c")
        notif_text.set("Video could not be downloaded")
    finally:
        url.delete(0, "end")


def downloadmp3(directory):
    file_name = directory.split("/")[-1]
    direc = "/".join(directory.split("/")[:-1])
    video_url = url.get()
    try:
        path = os.path.join(os.getcwd(), direc)
        os.chdir(path)

        youtube = pytube.YouTube(video_url)
        notif.config(fg="black")
        notif_text.set(f"Downloading \"{youtube.title}\"...")

        audio = youtube.streams.filter(adaptive=True, only_audio=True).first()
        audio.download(direc, filename=file_name.split(".")[0] + ".mp3")

        # pre, ext = file_name.split(".")
        # os.rename(file_name, pre + ".mp3")

        notif.config(fg="green")
        notif_text.set("Audio downloaded successfully")

    except Exception as e:
        print(e)
        notif.config(fg="#ff1c1c")
        notif_text.set("Audio could not be downloaded")

    finally:
        url.delete(0, "end")


root = tk.Tk()
root.title("Youtube Downloader")
root.resizable(False, False)

'''
STYLE
'''

style = ttk.Style()
style.theme_use("clam")

root["background"] = "#262626"

# Button style
style.configure("TButton", lightcolor="505050", darkcolor="#505050", background="#424242", foreground="#f0f0f0",
                font=("sans-serif", 15), borderwidth=0)
style.map("TButton",
          background=[("active", "#505050"), ("pressed", "#454545")],
          foreground=[("active", "#f0f0f0")])


# Entry style
style.configure("TEntry",
                fieldbackground="#151515",
                highlightthickness=1,
                highlightbackground="#222222",
                bordercolor="#262626",
                lightcolor="#808080",
                darkcolor="#151515",
                padding="10 1 1 1",
                insertcolor="#f0f0f0",
                foreground="#f0f0f0"
                )

style.map("TEntry",
          bordercolor=[("focus", "#fa4848")],
          lightcolor=[("focus", "#262626")]
          )


# Combobox style
style.configure("TCombobox",
                background="#424242",
                arrowcolor="#f0f0f0",
                fieldbackground="#424242",
                lightcolor="#424242",
                darkcolor="#424242",
                bordercolor="#424242",
                selectbackground="#424242",
                highlightbackground="#424242"
                )

style.map("TCombobox",
          fieldbackground=[("readonly", "#424242")],
          background=[("readonly", "#424242")],
          foreground=[("readonly", "#f0f0f0")],
          selectbackground=[("readonly", "#424242")]
          )

'''
WIDGETS
'''
root.columnconfigure(0, weight=1)
# Loading an image
yt_image = Image.open("assets/yt_logo.png").resize((50, 35))
yt_photo = ImageTk.PhotoImage(yt_image)

# Labels
title = tk.Label(root, image=yt_photo, compound="left", text=" YouTube Downloader", font=("sans-serif", 35),
                 fg="#f0f0f0", bg="#262626")
title.grid(row=0, pady=15, columnspan=4)

info = tk.Label(root, text="Type in url", fg="#f0f0f0",
                bg="#262626", font=("sans-serif", 13))
info.grid(row=1, pady=(10, 0), columnspan=4)

notif_text = tk.StringVar()
notif = tk.Label(textvariable=notif_text, bg="#262626")
notif.grid(row=4, columnspan=4)


# Entry
url = ttk.Entry(root,
                width=40,
                font=("sans-serif", 15),
                )

url.grid(row=2, ipady=10, padx=15, sticky="EW", columnspan=4)

# Combobox

format_combobox = ttk.Combobox(
    root, width=5, state="readonly", justify="center")
format_combobox["values"] = ("MP4", "MP3")
format_combobox.set("MP4")
format_combobox.grid(row=3, column=3, sticky="NSEW",
                     padx=(0, 15), ipady=10, pady=(30, 10))
format_combobox.option_add("*TCombobox*Listbox.background", "#505050")
format_combobox.option_add("*TCombobox*Listbox.font", ("sans-serif", 15))
format_combobox.option_add("*TCombobox*Listbox.foreground", "#f0f0f0")
format_combobox.option_add("*TCombobox*Listbox.selectBackground", "#f0f0f0")
format_combobox.option_add("*TCombobox*Listbox.selectForeground", "#505050")

# Convert Button
convert_button = ttk.Button(
    root, text="Convert", command=convert, takefocus=False)
convert_button.grid(row=3, pady=(30, 10), padx=15,
                    sticky="EW", ipady=10, columnspan=3)

root.mainloop()

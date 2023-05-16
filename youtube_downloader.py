from tkinter import Label
from PIL import Image, ImageTk
from pytube import YouTube
import tkinter as tk

download_window = None

def download_video():
    video_url = entry_url.get()
    try:
        if download_window is not None and download_window.winfo_exists():
            download_window.withdraw()
        youtube = YouTube(video_url)
        video = youtube.streams.get_highest_resolution()
        video.download()
        status_label.config(text="Видео успешно скачано!")
        if download_window is not None and download_window.winfo_exists():
            download_window.destroy()
    except Exception as e:
        status_label.config(text="Введите URL нужного вам видео")

def show_download_window():
    global download_window
    if download_window is not None and download_window.winfo_exists():
        return

    video_url = entry_url.get()
    try:
        youtube = YouTube(video_url)
        title = youtube.title
        duration = format_time(youtube.length)
        size = format_size(youtube.streams.get_highest_resolution().filesize)

        download_window = tk.Toplevel(root)
        download_window.title("Загрузка видео")

        download_window_label = tk.Label(download_window, text=f"Это видео называется: {title}\nЕго продолжительность: {duration}\nЕго приблизительный вес: {size}")
        download_window_label.pack()

        download_button = tk.Button(download_window, text="Да, скачать", command=download_video)
        download_button.pack()

        root.withdraw()  # Скрыть основное окно

        # Центрирование окна загрузки
        download_window.update()
        download_window_width = download_window.winfo_width()
        download_window_height = download_window.winfo_height()
        download_x = (download_window.winfo_screenwidth() - download_window_width) // 2
        download_y = (download_window.winfo_screenheight() - download_window_height) // 2
        download_window.geometry(f"{download_window_width}x{download_window_height}+{download_x}+{download_y}")

    except Exception as e:
        status_label.config(text="Введите URL нужного вам видео")

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def format_size(bytes):
    sizes = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while bytes >= 1024 and index < len(sizes) - 1:
        bytes /= 1024
        index += 1
    return f"{bytes:.2f} {sizes[index]}"

def handle_paste(event):
    if not entry_url.get():  # Проверка, есть ли уже вставленное содержимое
        content = root.clipboard_get()
        entry_url.delete(0, 'end')
        entry_url.insert(0, content)


root = tk.Tk()
    
root.title("Скачивание видео с YouTube")

# Установка фона
background_color = "#252525"
image = Image.new("RGB", (750, 300), background_color)
photo = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=photo)
background_label.image = photo
background_label.place(x=0, y=0)

# Установка фиксированного размера окна
root.geometry(f"{image.width}x{image.height}")

url_label = Label(root, text="URL видео:")
url_label.pack()

entry_url = tk.Entry(root, width=50)
entry_url.pack()

entry_url.bind("<Button-3>", lambda e: entry_url.event_generate("<<Paste>>"))
entry_url.bind("<<Paste>>", handle_paste)

download_button = tk.Button(root, text="Скачать", command=show_download_window)
download_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()

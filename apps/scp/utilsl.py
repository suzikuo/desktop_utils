import tkinter as tk
from tkinter import messagebox
import win32gui
import win32con


def enum_windows_callback(hwnd, window_list):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetParent(hwnd) == 0:
        title = win32gui.GetWindowText(hwnd)
        if title:
            window_list.append((hwnd, title))


def find_visible_windows():
    window_list = []
    win32gui.EnumWindows(enum_windows_callback, window_list)
    return window_list


def set_window_topmost(hwnd):
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0,
        0,
        0,
        0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
    )


def reset_window_topmost(hwnd):
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_NOTOPMOST,
        0,
        0,
        0,
        0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
    )


def open_window_selector():
    windows = find_visible_windows()
    window_selection = tk.Toplevel(root)
    window_selection.title("Select Window")

    topmost_window = None

    def on_button_click(hwnd, title):
        nonlocal topmost_window
        if topmost_window:
            reset_window_topmost(topmost_window)
        set_window_topmost(hwnd)
        topmost_window = hwnd
        messagebox.showinfo("Window Topmost", f"Window '{title}' is now topmost.")

    for hwnd, title in windows:
        frame = tk.Frame(window_selection, relief=tk.RAISED, borderwidth=1)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        button = tk.Button(
            frame, text=title, command=lambda h=hwnd, t=title: on_button_click(h, t)
        )
        button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


root = tk.Tk()
root.title("Window Handle Selector")

open_button = tk.Button(root, text="Open Window Selector", command=open_window_selector)
open_button.pack(padx=20, pady=20)

root.mainloop()

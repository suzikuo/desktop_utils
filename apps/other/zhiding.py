import subprocess
import time
import win32gui
import win32con

def enum_windows_callback(hwnd, window_list):
    # 获取窗口标题
    title = win32gui.GetWindowText(hwnd)
    if "Calculator" in title or "计算器" in title:  # 根据系统语言检查窗口标题
        window_list.append(hwnd)

def find_calculator_window():
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
def open_calculator():
    # 启动计算器
    subprocess.Popen("calc.exe")
    # 等待计算器启动
    time.sleep(1)
    # 查找计算器窗口
    window_list = find_calculator_window()
    if window_list:
        # 将计算器窗口置顶
        set_window_topmost(window_list[0])

import os
import json
import webview
import atexit

# 设置窗口的宽度和高度
window_width = 400
window_height = 800
# 计算窗口的位置
x_position = 1300  # 将窗口靠近右侧
y_position = 50  # 将窗口垂直居中


# 获取 Local AppData 路径
local_appdata_path = os.path.expanduser("~")

# # 要创建的文件夹和文件路径
folder_name = "mypwdmg"
mypwdmg_dir = os.path.join(local_appdata_path, folder_name)
# 检查文件夹是否存在，如果不存在则创建
if not os.path.exists(mypwdmg_dir):
    os.makedirs(mypwdmg_dir)


# Path to the localStorage file
local_storage_file = os.path.join(mypwdmg_dir, "localStorage_data.json")
print("the local storage file path is :", local_storage_file)
# In-memory storage for localStorage data
local_storage_data = {}


def localStorageChanged(data):
    """Handle changes to localStorage."""
    key = data["key"]
    value = data["value"]
    print(f"Updated in-memory localStorage: {key} : {value}")
    # Update in-memory data instead of writing to the file immediately
    local_storage_data[key] = value

    # print(f"Updated in-memory localStorage: {local_storage_data}")


def read_local_storage_data():
    """Read data from the localStorage file if it exists."""
    global local_storage_data
    try:
        if os.path.exists(local_storage_file):
            with open(local_storage_file, "r") as file:
                local_storage_data = json.load(file)
            print(f"Loaded data from {local_storage_file}")
        else:
            print("No existing localStorage file found. Starting with empty data.")
    except Exception as e:
        print(f"Error reading file: {e}")
        local_storage_data = {}


def flush_local_storage_to_file():
    """Write in-memory data to the file when the app exits."""
    try:
        with open(local_storage_file, "w") as file:
            json.dump(local_storage_data, file, indent=4)
        print(f"Flushed localStorage to {local_storage_file}")
    except Exception as e:
        print(f"Error saving data: {e}")


def onload_eval_js(window, data):
    """Inject the in-memory data into JavaScript's localStorage."""
    js_code = """
    let data = %s;  // 从 Python 获取的 data
    if (data) {
        for (let key in data) {
            if (data.hasOwnProperty(key)) {
                localStorage.setItem(key, data[key]);
            }
        }
    }
    // 原始的 localStorage.setItem
    const originalSetItem = localStorage.setItem;

    // 重写 setItem 方法
    localStorage.setItem = function(key, value) {
        // 调用原始的 setItem 方法
        originalSetItem.call(localStorage, key, value);

        // 通知 Python，localStorage 数据发生了变化
        window.pywebview.api.localStorageChanged({ key: key, value: value });
    };
    
    """ % json.dumps(data)
    window.evaluate_js(js_code)


def on_window_loaded(window):
    """Called when the window is loaded."""
    # Read data from the file and store it in localStorage
    read_local_storage_data()
    onload_eval_js(window, local_storage_data)


def main():
    """Create the window and start the webview."""
    # Create WebView window
    window = webview.create_window("My Passowd Manager - by suzikuo", "./front/index.html", width=window_width, height=window_height, x=x_position, y=y_position)

    # Expose the localStorageChanged function to JavaScript
    window.expose(localStorageChanged)

    # Add a callback for when the window is loaded
    window.events.loaded += lambda: on_window_loaded(window)

    # Register the function to flush data to the file when the app exits
    atexit.register(flush_local_storage_to_file)

    # Start the webview window
    webview.start()


if __name__ == "__main__":
    main()

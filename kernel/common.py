import subprocess

from kernel.settings import  config, main_config_file


def open_config_file(*args, **kwargs):
    """
    打开配置文件
    """
    subprocess.Popen(["cmd", "/c", "start", "", main_config_file])


def reload_config_file(*args, **kwargs):
    """
    重载配置文件
    """
    config.init()


def is_port_in_use(port):
    import subprocess

    result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
    output = result.stdout
    lines = output.split("\n")
    for line in lines:
        if str(port) in line and "LISTENING" in line:
            return True

    return False


def kill_process_using_port(port):
    try:
        result = subprocess.run(
            ["netstat", "-ano", "-p", "TCP"], capture_output=True, text=True
        )
        output = result.stdout
        for line in output.split("\n"):
            if f":{port}" in line:
                pid = line.split()[-1]
                if int(pid) == 0:
                    continue
                subprocess.run(["taskkill", "/F", "/PID", pid])
                print(f"Process with PID {pid} using port {port} has been terminated.")
    except subprocess.CalledProcessError:
        print("Error occurred while trying to execute commands.")


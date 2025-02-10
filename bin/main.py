import subprocess
import sys
import os

def open_new_terminal(script_name="your_script.py"):
    script_path = os.path.join(os.getcwd(), script_name)
    
    if sys.platform == "win32":
        subprocess.Popen(["cmd", "/k", "python", script_path], shell=True)
    elif sys.platform == "darwin":  # macOS
        subprocess.Popen(["osascript", "-e", f'tell application "Terminal" to do script "python3 {script_path}"'])
    else:  # Linux and Raspberry Pi
        try:
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"python3 {script_path}; exec bash"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            try:
                subprocess.Popen(["lxterminal", "-e", f"python3 {script_path}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except FileNotFoundError:
                print("No supported terminal found")

if __name__ == "__main__":
    # open_new_terminal("get_data_from_micro.py")
    open_new_terminal("process_to_coordinate.py")
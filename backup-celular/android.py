import subprocess
import os

# Define paths
android_path = "/sdcard/DCIM/Camera/"  # Most common
# OR (if it doesn't work)
# android_path = "/storage/emulated/0/DCIM/Escuela/"

script_dir = os.path.dirname(os.path.abspath(__file__))
adb_path = os.path.join(script_dir, "android/platform-tools/adb.exe")  # Windows

# List files on Android (optional)
print("Files on Android:")
subprocess.run([adb_path, "shell", "ls", android_path])
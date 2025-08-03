from io import TextIOWrapper
from subprocess import run, CompletedProcess
import os

# Define paths
android_path = "/sdcard/DCIM/Camera/"  # Most common
# OR (if it doesn't work)
# android_path = "/storage/emulated/0/DCIM/Escuela/"

script_dir = os.path.dirname(os.path.abspath(__file__))
adb_path = os.path.join(script_dir, "android/platform-tools/adb.exe")  # Windows
android_ip_port = 'COMPLETE'

# List files on Android (optional)
# print("Files on Android:")
# subprocess.run([adb_path, "shell", "ls", android_path])


def execute_adb_command(args: list, log: TextIOWrapper) -> CompletedProcess[str] | None:
    if (len(args) == 0):
        log.write('\nError: there are no arguments to execute adb.exe with')
        return None
    
    log.write(f'\nExecuting ./adb {' '.join(args)}')
    args.insert(0, adb_path)
    result: CompletedProcess[str] = run(args=args, capture_output=True, text=True)

    log.write("\nSTDOUT:\n")
    log.write(result.stdout)

    log.write("STDERR (if any):")
    log.write(result.stderr)
    log.write('\n\n')

    return result

def check_android_connected(result: CompletedProcess[str]) -> bool:
    lines = result.stdout.splitlines()
    if len(lines) != 3: 
        print(f'Error. Invalid number of lines: {len(lines)}')
        return False

    ip_line = lines[1].split()
    if len(ip_line) != 2: 
        print(f'Error. Invalid number of lines for ip line: {len(ip_line)}')
        return False
    
    if ip_line[1].lower() != 'device': 
        print(f'Error. The attached element is not a device: {ip_line[1]}')
        return False
    
    return True

def adb_connect(ip_port: str, log: TextIOWrapper) -> CompletedProcess[str]:
    return execute_adb_command(['connect', ip_port], log=log)

def adb_disconnect(log: TextIOWrapper) -> CompletedProcess[str]:
    return execute_adb_command(['disconnect'], log=log)

def adb_devices(log: TextIOWrapper) -> CompletedProcess[str]:
    return execute_adb_command(['devices'], log=log)


with open('log-android.txt', 'w', encoding="utf-8") as file:

    file.write('--- CONFIGURATION ----------------------------------------------------------')
    file.write(f'\nPath to adb.exe: {adb_path}')
    file.write(f'\nAndroid path: {android_path}')
    file.write(f'\nAndroid device`s IP and port: {android_ip_port}')
    file.write('\n----------------------------------------------------------------------------')

    file.write('\n\n--- EXECUTION --------------------------------------------------------------')

    result = adb_devices(log=file)
    connected = check_android_connected(result=result)

    if connected:
        print('Connected:', connected)
    else:
        print('Connected:', connected)
        adb_connect(android_ip_port, log=file)
        result = adb_devices(log=file)
        connected = check_android_connected(result=result)
        print('Connected:', connected)

    if connected: adb_disconnect(log=file)
    file.write('\n----------------------------------------------------------------------------')

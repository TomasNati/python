from io import TextIOWrapper
from subprocess import run, CompletedProcess
import os

android_path = "/sdcard/DCIM/Hablame/"  # Most common
android_ip_port = '192.168.1.56:45925'

class ADBInterface:
    def __init__(self, android_ip_port:str, logger: TextIOWrapper):
        self.logger = logger

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.__adb_path = os.path.join(script_dir, "android/platform-tools/adb.exe")  # Windows
        self.android_ip_port = android_ip_port

    def __execute_adb_command(self, args: list) -> CompletedProcess[str] | None:
        if (len(args) == 0):
            self.logger.write('\nError: there are no arguments to execute adb.exe with')
            return None
        
        self.logger.write(f'\nExecuting ./adb {' '.join(args)}')
        args.insert(0, self.__adb_path)
        result: CompletedProcess[str] = run(args=args, capture_output=True, text=True)

        self.logger.write("\nSTDOUT:\n")
        self.logger.write(result.stdout)

        if len(result.stderr) > 0: 
            self.logger.write("STDERR (if any):")
            self.logger.write(result.stderr)
            self.logger.write('\n\n')
        
        return result

    def check_android_connected(self, result: CompletedProcess[str]) -> bool:
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

    def connect(self, ip_port: str) -> CompletedProcess[str]:
        return self.__execute_adb_command(['connect', ip_port])

    def disconnect(self) -> CompletedProcess[str]:
        return self.__execute_adb_command(['disconnect'])

    def devices(self) -> CompletedProcess[str]:
        return self.__execute_adb_command(['devices'])
    
    def log_files_in_folder(self, path: str) -> None:
        args = ["shell", "ls", path]
        self.__execute_adb_command(args=args)


with open('log-android.txt', 'w', encoding="utf-8") as file:

    file.write('\n\n--- EXECUTION --------------------------------------------------------------')

    adb = ADBInterface(android_ip_port=android_ip_port, logger=file)

    result = adb.devices()
    connected = adb.check_android_connected(result=result)

    if connected:
        print('Connected:', connected)
    else:
        print('Connected:', connected)
        adb.connect(android_ip_port)
        result = adb.devices()
        connected = adb.check_android_connected(result=result)
        print('Connected:', connected)

    adb.log_files_in_folder(path=android_path)
    if connected: adb.disconnect()
    file.write('\n----------------------------------------------------------------------------')

from io import TextIOWrapper
from subprocess import run, CompletedProcess
import os

android_path = "/sdcard/DCIM/Hablame/"  # Most common
android_ip = '192.168.1.56'

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

    def __check_android_connected(self) -> bool:
        result = self.__execute_adb_command(['devices'])
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

    def connect(self) -> CompletedProcess[str]:
        port = input('Puerto: ')
        if not port: return
            
        retries = 0
        connected = False
        while not connected and retries < 3:
            retries += 1
            self.__execute_adb_command(['connect', f'{android_ip}:{port}'])
            connected = self.__check_android_connected()

        if not connected:
            print('Connection failed.')
        
    def disconnect(self) -> CompletedProcess[str]:
        return self.__execute_adb_command(['disconnect'])

    def log_files_in_folder(self, path: str) -> None:
        # - find /sdcard/YourFolderName: Starts searching in the target folder.
        # - -maxdepth 1: Limits the search to the top-level directory (no recursion).
        # - -type f: Filters to include only regular files (excludes directories).
        # - -exec ls -l {} \;: Runs ls -l on each file to show detailed info including modified date.
        # 📌 Example Output:
        # -rw-rw---- 1 user sdcard_rw  1024 Aug  4 22:30 file1.txt
        # -rw-rw---- 1 user sdcard_rw  2048 Aug  3 18:15 file2.jpg

        command = f"find {path} -maxdepth 1 -type f -exec ls -l {{}} \\;"
        args = ["shell", command]
        self.__execute_adb_command(args=args)


def get_menu_option(opciones_validas: list[str], logger: TextIOWrapper) -> str:
    try:
        opcion = ''
        
        while opcion not in opciones_validas:
            print('\nOpciones:')
            print('1: Conectarse')
            print('2: Listar archivos')
            print('q: Salir')
            opcion = input("Opción:")
    except Exception as e:
        logger.write('Error:', e)
        print('An error has ocurred.')
    finally:
        return opcion

def list_files_with_dates():
    """
    List files in current directory with their modification dates.
    
    Command: ls -l --time-style=+"%Y-%m-%d" | grep -v '^d' | awk '{print $6, $7}'
    
    Pipeline breakdown:
    1. ls -l --time-style=+"%Y-%m-%d"
       - Lists directory contents in long format
       - Formats dates as YYYY-MM-DD
       
    2. grep -v '^d'
       - Filters out directories (lines starting with 'd')
       - Only keeps regular files
       
    3. awk '{print $6, $7}'
       - Extracts and prints field 6 (date) and field 7 (filename)
       - Fields are space-separated
    
    Returns:
        Prints to stdout: Each line contains "YYYY-MM-DD filename"
        
    Example output:
        2025-08-05 script.sql
        2025-08-04 config.txt
        2025-08-03 readme.md
        
    Notes:
        - No sorting applied (files appear in filesystem order)
        - Only processes current directory (no subdirectories)
        - Date format is ISO 8601 compatible (YYYY-MM-DD)
    """
    pass

with open('log-android.txt', 'w', encoding="utf-8") as file:

    file.write('\n\n--- EXECUTION --------------------------------------------------------------')
    opciones_validas = ['1', '2', 'q']
    adb = ADBInterface(android_ip_port=android_ip, logger=file)

    opcion = '1'
    while opcion in opciones_validas:
        opcion = get_menu_option(opciones_validas=opciones_validas, logger=file)
        if opcion == '1':
            adb.connect()
            print('Opción ejecutada exitosamente')
        elif opcion == '2':
            adb.log_files_in_folder(path=android_path)
            print('Opción ejecutada exitosamente')
        elif opcion == 'q':
            adb.disconnect()
            opcion = ''
               
    file.write('\n----------------------------------------------------------------------------')

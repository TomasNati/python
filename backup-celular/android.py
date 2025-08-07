from io import TextIOWrapper
from subprocess import run, CompletedProcess
import os
from clases import Config, Celular

celulares = Config().celulares

android_path = "/sdcard/DCIM/Hablame/"  # Most common
android_ip = '192.168.1.56'

class ADBInterface:
    def __init__(self, android_ip_port:str, logger: TextIOWrapper):
        self.logger = logger

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.__adb_path = os.path.join(script_dir, "android/platform-tools/adb.exe")  # Windows
        self.android_ip_port = android_ip_port

    def __execute_adb_command(self, args: list, capture_output: bool = True, text: bool = True) -> CompletedProcess[str] | None:
        if (len(args) == 0):
            self.logger.write('\nError: there are no arguments to execute adb.exe with')
            return None
        
        self.logger.write(f'\nExecuting ./adb {' '.join(args)}')
        self.logger.flush()  # Flush immediately to see command execution
        
        args.insert(0, self.__adb_path)
        result: CompletedProcess[str] = run(args=args, capture_output=capture_output, text=text)

        if text:
            self.logger.write("\nSTDOUT:\n")
            self.logger.write(result.stdout)

            if len(result.stderr) > 0: 
                self.logger.write("STDERR (if any):")
                self.logger.write(result.stderr)
                self.logger.write('\n\n')
            
            self.logger.flush()  # Flush after writing output
            
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
    
    def parear_con_dispositivo(self) -> None:
        android_address = input('Ingrese ip:puerto del dispositivo:')
        if not android_address: return
        self.__execute_adb_command(['pair', android_address], capture_output=False, text=False)

    def __inner_connect(self, address: str) -> bool:
        retries = 0
        connected = False
        while not connected and retries < 3:
            retries += 1
            self.__execute_adb_command(['connect', address])
            connected = self.__check_android_connected()
        
        return connected


    def connect(self) -> bool:
        connected = self.__check_android_connected()
        if connected: return True

        connected = self.__inner_connect(self.android_ip_port)
        if connected: return True

        print(f'La conexión falló para {self.android_ip_port}')
        alt_address = input('Ingrese un <ip:puerto> alternativa: ')            
        connected = self.__inner_connect(alt_address)
        
        if not connected: print('La conexión falló para el <ip:puerto> ingresado')

        return connected
        
    def disconnect(self) -> CompletedProcess[str]:
        return self.__execute_adb_command(['disconnect'])

    def log_files_in_folder(self, path: str) -> None:
        """
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

        command2 = f"find {path} -maxdepth 1 -type f -exec ls -l {{}} \\;"
        args = ["shell", command2]
        result = self.__execute_adb_command(args=args)
        
        if result is None or result.stdout is None: return

        files = list()
        for line in result.stdout.splitlines():
            date, _, filename = line.split(maxsplit=8)[5:8]
            files.append((date, filename))

        for date, filename in files:
            self.logger.write(f"{date} {filename}")
            self.logger.write('\n')
        self.logger.flush()

def get_menu_option(opciones_validas: list[str], logger: TextIOWrapper) -> str:
    try:
        opcion = ''
        
        while opcion not in opciones_validas:
            print('\nOpciones:')
            print('1: Conectarse')
            print('2: Listar archivos')
            print('3: Parear con el dispositivo')
            print('q: Salir')
            opcion = input("Opción:")
    except Exception as e:
        logger.write('Error:', e)
        print('An error has ocurred.')
    finally:
        return opcion
    
def elegir_celular() -> Celular | None:
    print('Celulares:')
    for index, celular in enumerate(celulares):
        print(f'  ({index + 1}) {celular.name}')
    user_input = input('\nElige el celular, o cualquier otra tecla para salir: ')
    try:
        cel_index = int(user_input)
        if cel_index > 0 and cel_index <= len(celulares):
            return celulares[cel_index - 1] 
    except:
        return None

def main(): 
    celular = elegir_celular()
    if celular is None: return

    with open('log-android.txt', 'w', encoding="utf-8") as file:

        file.write('\n\n--- EXECUTION --------------------------------------------------------------')
        opciones_validas = ['1', '2', '3', 'q']
        adb = ADBInterface(android_ip_port=celular.address(), logger=file)

        opcion = '1'
        while opcion in opciones_validas:
            opcion = get_menu_option(opciones_validas=opciones_validas, logger=file)
            if opcion == '1':
                adb.connect()
                print('Opción ejecutada exitosamente')
            elif opcion == '2':
                adb.log_files_in_folder(path=android_path)
                print('Opción ejecutada exitosamente')
            elif opcion == '3':
                adb.parear_con_dispositivo()
                print('Opción ejecutada exitosamente')
            elif opcion == 'q':
                adb.disconnect()
                opcion = ''
                
        file.write('\n----------------------------------------------------------------------------')


main()

import logging
import os
import json
import stat
import datetime
import shutil
from abc import ABC, abstractmethod
from subprocess import CompletedProcess, TimeoutExpired, run
import console
import re

logger = logging.getLogger(__name__)

class Dispositivo(ABC):
    def __init__(self, init_name: str, init_paths: list[str], destination: str):
        self.name = init_name
        self.paths = init_paths
        self.destination = destination

    @abstractmethod
    def get_paths(self) -> list[str]:
        pass
    
    @abstractmethod
    def get_files_per_year(self, path: str, year_from: int | None) -> dict | None:
        pass

    @abstractmethod
    def copy_if_not_exists(self, file_info: tuple[str, str], dest_folder: str) -> str:
        pass
    
class Kindle(Dispositivo):
    def __init__(self, init_name: str, init_paths: list[str], destination: str):
        super().__init__(init_name=init_name, init_paths=init_paths, destination=destination)

    def __is_hidden(attributes: int) -> bool:
        return bool(attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    
    def get_paths(self) -> list[str]:
        paths = []
        for path in self.paths:
            full_path = f'{self.name}{path}'
            paths.append(full_path)
            
        return paths
    
    def get_files_per_year(self, path: str, year_from: int | None) -> dict | None:
        if not os.path.exists(path):
            print(f'Path does not exists: {path}')
            return None
        
        files_per_year = dict()

        for item in os.scandir(path):
            file_stats = item.stat()
            
            if self.__is_hidden(file_stats.st_file_attributes): continue
            if item.is_dir(): continue

            if item.is_file:
                file_name = item.name
                created_date = datetime.datetime.fromtimestamp(file_stats.st_mtime)
                created_year = created_date.year

                if (year_from != None and created_year < year_from): continue

                if not created_year in files_per_year:
                    files_per_year[created_year] = []
                files_per_year[created_year].append((file_name, f'{path}\\{file_name}'))

        files_per_year = dict(sorted(files_per_year.items(), reverse=True))
        
        return files_per_year
    
    def copy_if_not_exists(self, file_info: tuple[str, str], dest_folder: str) -> str:
        (filename, src_file) = file_info

        os.makedirs(dest_folder, exist_ok=True)
        dest_file = os.path.join(dest_folder, filename)

        if not os.path.exists(dest_file):
            shutil.copy2(src_file, dest_file)
            return f"Copied: {filename}"
        else:
            return f"Skipped (already exists): {filename}"
    
class Celular(Dispositivo):
    def __init__(self, init_name: str, init_paths: list[str], destination: str, ip: str, port: int):
        super().__init__(init_name=init_name, init_paths=init_paths, destination=destination)
        self.ip = ip
        self.port = port

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.__adb_path = os.path.join(script_dir, "android/platform-tools/adb.exe")  # Windows

    def __execute_adb_command(self, 
                              args: list, 
                              capture_output: bool = True, 
                              text: bool = True, 
                              timeout: int = 5,
                              log_stdout: bool = False) -> CompletedProcess[str] | None:
        if (len(args) == 0):
            logger.error('Error: there are no arguments to execute adb.exe with')
            return None
        
        logger.info(f'Executing ./adb {' '.join(args)}')
        
        args.insert(0, self.__adb_path)
        try:
            result: CompletedProcess[str] = run(args=args, capture_output=capture_output, text=text, timeout=timeout)
        except TimeoutExpired:
            logger.error(f"Command timed out after {timeout} seconds")
            return None

        if text:
            if log_stdout and len(result.stdout)> 0:
                logger.info(result.stdout)

            if len(result.stderr) > 0: 
                logger.error(result.stderr)
            
        return result

    def __check_android_connected(self) -> bool:
        result = self.__execute_adb_command(['devices'], log_stdout=True)
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
        self.__execute_adb_command(['pair', android_address], capture_output=False, text=False, timeout=30)

    def __inner_connect(self, address: str) -> bool:
        retries = 0
        connected = False
        while not connected and retries < 3:
            retries += 1
            result = self.__execute_adb_command(['connect', address], timeout=10, log_stdout=True)
            connected = result is not None and result.stdout is not None and 'connected to' in result.stdout
        
        return connected
    
    def _get_date_and_filename(self, line:str, dir_path: str) -> tuple[str, str]:
        parts = line.split(dir_path)
        attributes, filename = parts
        fullpath = f'{dir_path}{filename}'
        date = attributes.split()[-2]

        return date, fullpath

    def connected(self) -> bool:
        return self.__check_android_connected()

    def connect(self) -> tuple[bool, dict]:
        connected = self.__check_android_connected()
        if connected: return [True, {}]

        connected = self.__inner_connect(f'{self.ip}:{self.port}')
        if connected: return [True, {}]

        texto = input(
              f'La conexión falló para {self.ip}:{self.port}\n'
              ' - Ingresar ip. Tipear 1 <ip>\n'
              ' - Ingresar puerto. Tipear 2 <port> \n'
              ' - Ingresar ip:puerto. Tipear 3 <ip:port>\n' 
              'Opción: '
            )

        opcion = texto[0]
        updates = {}
        if opcion == '1':
            updates['ip'] = texto.split(' ')[1]
            alt_address = f'{updates['ip']}:{self.port}'
        elif opcion == '2':
            updates['port'] = texto.split(' ')[1]
            alt_address = f'{self.ip}:{updates['port']}'
        elif opcion == '3':
            updates['ip'], updates['port'] = texto.split(' ')[1].split(':')
            alt_address = f'{updates['ip']}:{updates['port']}'
        else:
            return False

        connected = self.__inner_connect(alt_address)

        if connected: return [True, updates]
        else: 
            console.print_error('La conexión falló para el <ip:puerto> ingresado')
            return [False, updates]

    def disconnect(self) -> CompletedProcess[str]:
        return self.__execute_adb_command(['disconnect'])

    def address(self) -> str:
        return f'{self.ip}:{self.port}'
    
    def get_paths(self) -> list[str]:
        paths = []
        for path in self.paths:
            paths.append(path)
            
        return paths
    
    def get_files_per_year(self, path: str, year_from: int | None) -> dict | None:
        try:
            command2 = f"find '{path}' -maxdepth 1 -type f -exec ls -l {{}} \\;"
            args = ["shell", command2]
            result = self.__execute_adb_command(args=args, timeout=60)
            
            if result is None or result.stdout is None: return

            files = list()
            for line in result.stdout.splitlines():
                date, filepath = self._get_date_and_filename(line, path)
                files.append((date, filepath))

            files_per_year = dict()
            for date, filepath in files:
                year = date.split('-')[0]
                if year_from is not None and int(year) < year_from: continue
                if not year in files_per_year:
                    files_per_year[year] = []

                filename = filepath.split('/')[-1]
                files_per_year[year].append((filename, filepath))

            files_per_year = dict(sorted(files_per_year.items(), reverse=True))

            return files_per_year
        except Exception as e:
            logger.error(f'An error has occurred on log_files_in_folder: ', e)
            return {}

    def copy_if_not_exists(self, file_info: tuple[str, str], dest_folder: str) -> str:
        filename, filepath = file_info
        
        os.makedirs(dest_folder, exist_ok=True)
        dest_file = os.path.join(dest_folder, filename)

        if not os.path.exists(dest_file):
            args = ["pull", filepath, f'{dest_folder}/{filename}']
            self.__execute_adb_command(args=args, log_stdout=True)
            return 'Copied'
        else:
            logger.info(f"Skipped (already exists): {filename}")
            return 'Skipped'

class Config:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(script_dir, "config.json")

        with open(self.config_path, 'r') as f:
            CONFIG = json.load(f)

            self.celulares: list[Celular] = []
            for celular_config in CONFIG['celulares']:
                celular = Celular(init_name=celular_config['name'],
                                init_paths=celular_config['paths'],
                                destination=celular_config['destination'],
                                ip=celular_config['ip'],
                                port=celular_config['port'])
                self.celulares.append(celular)

            self.kindle = Kindle(CONFIG['kindle']['name'], 
                                CONFIG['kindle']['paths'],
                                CONFIG['kindle']['destination'])

    def actualizar_celular_propiedad(self, celular: Celular, props_values: dict[str, str | int]) -> Celular | None:
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            celular_data = next((item for item in config['celulares'] if item['name'] == celular.name), None)
            if not celular_data:
                print(f"❌ Error: Celular {celular.name} not found in config!")
                return

            for prop, value in props_values.items():
                celular_data[prop] = value

            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)

            print("✅ Config updated successfully!")

        except FileNotFoundError:
            print(f"❌ Error: {self.config_path} not found!")
        except json.JSONDecodeError:
            print(f"❌ Error: Invalid JSON in {self.config_path}!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        finally:
            print("🔄 Reloading config...")
            self.__init__()
            celular_actualizado = next((cel for cel in self.celulares if cel.name == celular.name), None)
            return celular_actualizado
        
    def get_device(self, tipo: str, name: str | None) -> Dispositivo | None:
        if tipo is None: return None
        if tipo.lower() == 'kindle':
            return self.kindle
        elif tipo.lower() == 'celular' and name is not None:
            celular = next((cel for cel in self.celulares if cel.name.lower() == name.lower()), None)
            return celular

config = Config()

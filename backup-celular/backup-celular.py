# 1. Definir los paths de los celulare de donde leer archivos. O usar un file dialog? Tal vez esto sea mejor.
#    -> Dejarlos en un archivo de configuración, y que se pueda cambiar.
# 2. Definir path para backup destino. Permite con un file dialog? Tipo C:\Backups\Celulares\Andres
# 3. Permitir ingresar a partir de que año considerar los archivos.
# 4. Para cada path de 1.
#     a. Obtengo el año del archivo
#     b. Lo copio en la carpeta de 2\año del archivo. Si existe el archivo, saltear la copia.
#     c. Informar cuantos archivos se copiaron por año
from config import  CONFIG
import os
import datetime
import stat
import shutil

class Dispositivo:
    def __init__(self, init_names: list[str], init_paths: list[str], destination: str):
        self.names: list[str] = init_names
        self.paths: list[str] = init_paths
        self.destination = destination

    def get_paths(self) -> list[str]:
        paths = []
        for name in self.names:
            for path in self.paths:
                full_path = f'{name}{path}'
                paths.append(full_path)
        
        return paths

class Config:
    def __init__(self):
        self.celular = Dispositivo(CONFIG['celular']['names'], 
                               CONFIG['celular']['paths'],
                               CONFIG['celular']['destination'])
        self.kindle = Dispositivo(CONFIG['kindle']['names'], 
                               CONFIG['kindle']['paths'],
                               CONFIG['kindle']['destination'])
        
config = Config()


def is_hidden(attributes: int) -> bool:
    return bool(attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def get_files_per_year(path: str) -> dict:
    if not os.path.exists(path):
        print(f'Path does not exists: {path}')
        return None
    
    files_per_year = dict()

    for item in os.scandir(path):
        file_stats = item.stat()
        
        if is_hidden(file_stats.st_file_attributes): continue
        if item.is_dir(): continue

        if item.is_file:
            file_name = item.name
            created_date = datetime.datetime.fromtimestamp(file_stats.st_mtime)
            created_year = created_date.year
            if not created_year in files_per_year:
                files_per_year[created_year] = []
            files_per_year[created_year].append((file_name, f'{path}\\{file_name}'))

    files_per_year = dict(sorted(files_per_year.items(), reverse=True))
    
    return files_per_year


def copy_if_not_exists(file_info: tuple[str, str], dest_folder: str) -> str:
    (filename, src_file) = file_info

    os.makedirs(dest_folder, exist_ok=True)
    dest_file = os.path.join(dest_folder, filename)

    if not os.path.exists(dest_file):
        shutil.copy2(src_file, dest_file)
        return f"Copied: {filename}"
    else:
        return f"Skipped (already exists): {filename}"


def backup_files(source_path:str, dest_folder: str, log_file: str) -> None:
    files_per_year = get_files_per_year(source_path)

    if files_per_year == None: return

    with open(log_file, 'w', encoding="utf-8") as file:
        file.write(f'Writing files in folder: {source_path} to base destination: {dest_folder}\n')
        for year in files_per_year:
            copied = 0
            skipped = 0
            files = files_per_year[year]
            file.write(f'\n--- YEAR {year} -------------------------------------------------------')
            
            for file_info in files:
                log_res = copy_if_not_exists(file_info, f'{dest_folder}\\{year}')
                
                if log_res.lower().find('skipped') > -1: skipped += 1
                else: copied +=1 

                try:
                    file.write(f'\n{log_res}')
                except Exception as e:
                    print(f'An error ocurred when printing line: {log_res}', e)

            file.write(f'\n-----------------------------------------------------------------------\n')

            print(f'Year {year} - Copied: {copied} files - Skipped: {skipped} files')    

def main():
    try:
        device = input('Dispositivo a copiar\n 1.Celular Andrés\n 2.Kindle\nIngrese el número: ')
        if device == '1': device = config.celular
        elif device =='2': device = config.kindle
        else:
            print('Invalid device')
            return

        log_index = 1
        for source_path in device.get_paths():
            backup_files(source_path, device.destination, f'log-file{log_index}.txt')
            log_index +=1


    except Exception as e:
        print('An error has occurred:', e)

main()
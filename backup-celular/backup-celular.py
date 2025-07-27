# 1. Definir los paths de los celulare de donde leer archivos. O usar un file dialog? Tal vez esto sea mejor.
#    -> Dejarlos en un archivo de configuración, y que se pueda cambiar.
# 2. Definir path para backup destino. Permite con un file dialog? Tipo C:\Backups\Celulares\Andres
# 3. Permitir ingresar a partir de que año considerar los archivos.
# 4. Para cada path de 1.
#     a. Obtengo el año del archivo
#     b. Lo copio en la carpeta de 2\año del archivo. Si existe el archivo, saltear la copia.
#     c. Informar cuantos archivos se copiaron por año
from config import WINDOWS_PATH, CONFIG
import os
import datetime
import stat
import shutil

class Celular:
    def __init__(self, init_names: list[str], init_paths: list[str], destination: str):
        self.names: list[str] = init_names
        self.paths: list[str] = init_paths
        self.destination = destination

class Config:
    def __init__(self):
        self.celular = Celular(CONFIG['celular']['names'], 
                               CONFIG['celular']['paths'],
                               CONFIG['celular']['destination'])

    def get_paths(self) -> list[str]:
        paths = []
        for name in self.celular.names:
            for path in self.celular.paths:
                full_path = f'{WINDOWS_PATH}{name}{path}'
                paths.append(full_path)
        
        return paths

config = Config()


test_path = 'C:\\Users\\Andres\\Backups\\Kindle\\documents'

def is_hidden(attributes: int) -> bool:
    return bool(attributes & stat.FILE_ATTRIBUTE_HIDDEN)

def get_files_per_year(path: str) -> None:
    if not os.path.exists(path):
        print(f'Path does not exists: {path}')
        return
    
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


def copy_if_not_exists(file_info: tuple[str, str], dest_folder: str) -> None:
    (filename, src_file) = file_info

    os.makedirs(dest_folder, exist_ok=True)
    dest_file = os.path.join(dest_folder, filename)

    if not os.path.exists(dest_file):
        shutil.copy2(src_file, dest_file)
        print(f"Copied: {filename}")
    else:
        print(f"Skipped (already exists): {filename}")


files_per_year = get_files_per_year(test_path)

for year in files_per_year:
    files = files_per_year[year]
    for file_info in files:
        copy_if_not_exists(file_info, f'{config.celular.destination}\\{year}')



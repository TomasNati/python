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

class Celular:
    def __init__(self, init_names: list[str], init_paths: list[str]):
        self.names: list[str] = init_names
        self.paths: list[str] = init_paths

class Config:
    def __init__(self):
        self.celular = Celular(CONFIG['celular']['names'], CONFIG['celular']['paths'])

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

def get_dir_properties(path: str) -> None:
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
            files_per_year[created_year].append(file_name)

    files_per_year = dict(sorted(files_per_year.items(), reverse=True))

    total_number_of_files = 0
    for year in files_per_year:
        files_amount = len(files_per_year[year])
        if files_amount > 1:
            print(f'There are {files_amount} files for year {year}')
        else:
            print(f'There is {files_amount} file for year {year}')
        total_number_of_files += files_amount

    print(f'\nTotal number of files: {total_number_of_files}')


get_dir_properties(test_path)



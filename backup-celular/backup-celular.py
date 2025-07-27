# 1. Definir los paths de los celulare de donde leer archivos. O usar un file dialog? Tal vez esto sea mejor.
#    -> Dejarlos en un archivo de configuración, y que se pueda cambiar.
# 2. Definir path para backup destino. Permite con un file dialog? Tipo C:\Backups\Celulares\Andres
# 3. Permitir ingresar a partir de que año considerar los archivos.
# 4. Para cada path de 1.
#     a. Obtengo el año del archivo
#     b. Lo copio en la carpeta de 2\año del archivo. Si existe el archivo, saltear la copia.
#     c. Informar cuantos archivos se copiaron por año
from config import WINDOWS_PATH, CONFIG

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

for path in config.get_paths():
    print(path)




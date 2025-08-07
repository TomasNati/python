from config import CONFIG

class Dispositivo:
    def __init__(self, init_name: str, init_paths: list[str], destination: str):
        self.name = init_name
        self.paths = init_paths
        self.destination = destination

    def get_paths(self) -> list[str]:
        paths = []
        for path in self.paths:
            full_path = f'{self.name}{path}'
            paths.append(full_path)
            
        
        return paths
    
class Celular(Dispositivo):
    def __init__(self, init_name: str, init_paths: list[str], destination: str, ip: str, port: int):
        super().__init__(init_name=init_name, init_paths=init_paths, destination=destination)
        self.ip = ip
        self.port = port


class Config:
    def __init__(self):
        self.celulares: list[Celular] = []
        for celular_config in CONFIG['celulares']:
            celular = Celular(init_name=celular_config['name'],
                              init_paths=celular_config['paths'],
                              destination=celular_config['destination'],
                              ip=celular_config['ip'],
                              port=celular_config['port'])
            self.celulares.append(celular)

        self.kindle = Dispositivo(CONFIG['kindle']['name'], 
                               CONFIG['kindle']['paths'],
                               CONFIG['kindle']['destination'])
        
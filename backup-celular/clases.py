import os
import json

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

    def address(self) -> str:
        return f'{self.ip}:{self.port}'


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

            self.kindle = Dispositivo(CONFIG['kindle']['name'], 
                                CONFIG['kindle']['paths'],
                                CONFIG['kindle']['destination'])
            
    def actualizar_celular_port(self, celular: Celular, new_port: str) -> None:
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
            # . Identificar el celular en el json
            # . Cambiar el puerto
            # . Grabar. Es posible que pueda usar un método general, donde ip o port sean un parámetro, y new_value lo que se les asigna
        
def probar(): 
    # 2. Load, modify, and save the config
    try:
        # Read config
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Modify config (example: update first entry's IP and Port)
        config['celulares'][0]['ip'] = '192.168.1.100'
        config['celulares'][0]['port'] = 5678

        # Save updated config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)

        print("✅ Config updated successfully!")
    except FileNotFoundError:
        print(f"❌ Error: {config_path} not found!")
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {config_path}!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
            
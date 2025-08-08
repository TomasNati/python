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

      
   
            
from io import TextIOWrapper
from clases import ADBInterface, Config, Celular
import console
import logging
logger = logging.getLogger(__name__)

config = Config()
android_path = "/sdcard/DCIM/Hablame/"  # Most common


def get_menu_option(opciones_validas: list[str]) -> str:
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
        logger.error('Error:', e)
        print('An error has ocurred.')
    finally:
        return opcion
    
def elegir_celular() -> Celular | None:
    print('Celulares:')
    for index, celular in enumerate(config.celulares):
        print(f'  ({index + 1}) {celular.name}')
    user_input = input('\nElige el celular, o cualquier otra tecla para salir: ')
    try:
        cel_index = int(user_input)
        if cel_index > 0 and cel_index <= len(config.celulares):
            return config.celulares[cel_index - 1] 
    except:
        return None

def main(): 
    celular = elegir_celular()
    if celular is None: return

    logging.basicConfig(
        filename='backup.log', 
        level=logging.INFO, 
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M'
    )

    logger.info('\n\n--- EXECUTION --------------------------------------------------------------')
    opciones_validas = ['1', '2', '3', 'q']
    adb = ADBInterface(celular=celular)
    connected = adb.connected()

    if connected: console.print_info('Status: connected')
    else: console.print_error('Status: disconnected')

    opcion = '1'
    while opcion in opciones_validas:
        opcion = get_menu_option(opciones_validas=opciones_validas)
        if opcion == '1':
            adb.connect()
            print('Opción ejecutada exitosamente')
        elif opcion == '2':
            files_per_year = adb.log_files_in_folder(path=celular.paths[0])
            for year in files_per_year:
                logger.info(f'------ YEAR {year} -----------------')
                files = files_per_year[year]
                for file in files:
                    logger.info(f'File path: {file}')

            print('Opción ejecutada exitosamente')
        elif opcion == '3':
            adb.parear_con_dispositivo()
            print('Opción ejecutada exitosamente')
        elif opcion == 'q':
            adb.disconnect()
            opcion = ''
            
    logger.info('\n----------------------------------------------------------------------------')


if __name__ == '__main__':
    main()

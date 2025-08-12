from clases import Celular, Dispositivo, config
import logging
import console

logger = logging.getLogger(__name__)

def safe_to_int(s: str) -> int | None:
    return int(s) if s.isdigit() else None

def backup_files(device: Dispositivo, source_path:str, dest_folder: str,year_from: int | None) -> None:
    files_per_year = device.get_files_per_year(source_path, year_from)

    if files_per_year == None: return

    logger.info(f'Writing files in folder: {source_path} to base destination: {dest_folder}\n')
    for year in files_per_year:
        copied = 0
        skipped = 0
        files = files_per_year[year]
        logger.info(f'\n--- YEAR {year} -------------------------------------------------------')
        
        for file_info in files:
            log_res = device.copy_if_not_exists(file_info=file_info,dest_folder=f'{dest_folder}/{year}')
            
            if log_res.lower().find('skipped') > -1: skipped += 1
            else: copied +=1 

            try:
                logger.info(f'\n{log_res}')
            except Exception as e:
                logger.error(f'An error ocurred when printing line: {log_res}', e)

        logger.info(f'\n-----------------------------------------------------------------------\n')

        logger.info(f'Year {year} - Copied: {copied} files - Skipped: {skipped} files')  

def get_menu_option(opciones_validas: list[str]) -> str:
    try:
        opcion = ''
        
        while opcion not in opciones_validas:
            print('\nOpciones:')
            print('1: Conectarse')
            print('2: Hacer backup de archivos')
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

    logging.basicConfig(
        filename='backup.log', 
        level=logging.INFO, 
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M'
    )

    try:
        device = input('Dispositivo a copiar\n 1.Celular \n 2.Kindle\nIngrese el número: ')
        if device == '1': 
            celular = elegir_celular()
            if celular is None: return
            device = celular

            opciones_validas = ['1', '2', '3', 'q']
            connected = celular.connected()

            if connected: console.print_info('Status: connected')
            else: console.print_error('Status: disconnected')

            opcion = '1'
            while opcion in opciones_validas:
                opcion = get_menu_option(opciones_validas=opciones_validas)
                if opcion == '1':
                    _, updates = celular.connect()
                    if updates:
                        config.actualizar_celular_propiedad(celular, props_values=updates)
                    print('Opción ejecutada exitosamente')
                elif opcion == '2':
                    copy_from_year = input('Copiar a partir del año (<Enter> ignora este filtro): ')
                    year_from = safe_to_int(copy_from_year)

                    log_index = 1
                    for source_path in device.get_paths():
                        backup_files(device, source_path, device.destination, year_from)
                        log_index +=1

                elif opcion == '3':
                    celular.parear_con_dispositivo()
                    print('Opción ejecutada exitosamente')
                elif opcion == 'q':
                    celular.disconnect()
                    opcion = ''

        elif device =='2':
            device = config.get_device('kindle')
            copy_from_year = input('Copiar a partir del año (<Enter> ignora este filtro): ')
            year_from = safe_to_int(copy_from_year)

            log_index = 1
            for source_path in device.get_paths():
                backup_files(device, source_path, device.destination, year_from)
                log_index +=1
        else:
            print('Invalid device')
            return

    except Exception as e:
        print('An error has occurred:', e)

main()

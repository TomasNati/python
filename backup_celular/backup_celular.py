from clases import Celular, Dispositivo, config
import logging
import console
import asyncio
import itertools

logger = logging.getLogger(__name__)

def safe_to_int(s: str) -> int | None:
    return int(s) if s.isdigit() else None

async def spinner(msg_func):
    max_length = 80
    try:
        for char in itertools.cycle('|/-\\'):
            msg = msg_func()
            max_length = max(len(msg), max_length)
            print(f'\r{msg} {char}', end='', flush=True)
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        # Clear the line on cancel
        print('\r' + ' ' * (max_length + 2) + '\r', end='', flush=True)
        raise


async def get_files_per_year_from_device(device: Dispositivo, source_path:str, year_from: int | None) ->dict | None:
    files = await asyncio.to_thread(device.get_files_per_year, source_path, year_from)
    return files

async def copy_files_for_year(device: Dispositivo, files:list, dest_folder: str, year: int, progress: dict) -> None:
  
   for file_info in files:
        log_res = await asyncio.to_thread(device.copy_if_not_exists, file_info=file_info,dest_folder=f'{dest_folder}/{year}')
        
        if log_res.lower().find('skipped') > -1: progress['skipped'] += 1
        elif log_res.lower().find('timeout') > -1: progress['timeout'] += 1
        else: progress['copied'] +=1 

        try:
            if device.name == config.kindle.name: logger.info(f'\n{log_res}')
        except Exception as e:
            logger.error(f'An error ocurred when printing line: {log_res}', e)
       

async def backup_files(device: Dispositivo, source_path:str, dest_folder: str,year_from: int | None) -> None:
    print(f'\nGetting files from {source_path}{f' - Year: {year_from}' if year_from is not None else ''}')
    spin_read = asyncio.create_task(spinner(lambda: f'📂 Processing... '))
    files_per_year = await get_files_per_year_from_device(device=device, source_path=source_path, year_from=year_from)
    spin_read.cancel()
    await asyncio.sleep(0.1)

    if files_per_year == None: return

    line = f'Writing files to base destination: {dest_folder}'
    logger.info(line)
    print(f'\n{line}')

    for year in files_per_year:
        files = files_per_year[year]
        line = f'--- YEAR {year} -------------------------------------------------------'
        logger.info(line)
        print(f'\n{line}')

        progress = {
            'total': len(files),
            'copied': 0,
            'skipped': 0,
            'timeout': 0
        }

        spin_copy = asyncio.create_task(spinner(lambda: f"📤 Copied: {progress['copied']} files - Skipped: {progress['skipped']} files - Timeout: {progress['timeout']} files"))
        await copy_files_for_year(device=device, files=files, dest_folder=dest_folder, year=year, progress=progress)
        spin_copy.cancel()
        await asyncio.sleep(0.1)

        line =  f"Copied: {progress['copied']} files - Skipped: {progress['skipped']} files - Timeout: {progress['timeout']} files"
        logger.info(line)
        print(line)

    print("✅ Backup completed")

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
                        asyncio.run(backup_files(device, source_path, device.destination, year_from))
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
                asyncio.run(backup_files(device, source_path, device.destination, year_from))
                log_index +=1
        else:
            print('Invalid device')
            return

    except Exception as e:
        print('An error has occurred:', e)

main()

from clases import Dispositivo, config

def safe_to_int(s: str) -> int | None:
    return int(s) if s.isdigit() else None

def backup_files(device: Dispositivo, source_path:str, dest_folder: str, log_file: str, year_from: int | None) -> None:
    files_per_year = device.get_files_per_year(source_path, year_from)

    if files_per_year == None: return

    with open(log_file, 'w', encoding="utf-8") as file:
        file.write(f'Writing files in folder: {source_path} to base destination: {dest_folder}\n')
        for year in files_per_year:
            copied = 0
            skipped = 0
            files = files_per_year[year]
            file.write(f'\n--- YEAR {year} -------------------------------------------------------')
            
            for file_info in files:
                log_res = device.copy_if_not_exists(file_info, f'{dest_folder}\\{year}')
                
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
        if device == '1': 
            device = config.get_device('celular', 'andres')
        elif device =='2':
            device = config.get_device('kindle')
        else:
            print('Invalid device')
            return
        
        copy_from_year = input('Copiar a partir del año (<Enter> ignora este filtro): ')
        year_from = safe_to_int(copy_from_year)

        log_index = 1
        for source_path in device.get_paths():
            backup_files(device, source_path, device.destination, f'log-file{log_index}.txt', year_from)
            log_index +=1


    except Exception as e:
        print('An error has occurred:', e)

main()
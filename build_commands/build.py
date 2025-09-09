import json
import os
import sys
import pyperclip

# build command: pyinstaller --onefile --add-data "solutions.json;." build.py

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Running as script, use script directory
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

# Use the helper function to get the config path
config_path = get_resource_path("solutions.json")

def app():
    with open(config_path, 'r') as f:
        solutions = json.load(f)

    solutions_sorted = sorted(solutions["solutions"])

    print('\nSolutions:')
    for index, solution in enumerate(solutions_sorted, 1):
        print(f' ({index}) {solution}')

    solution = input('Type <solution number> [b|d] <tag> [d|i|u]\n' \
    'For example: 1 b my-tag d\n' \
    '> ')
    try:
        items = solution.split()
        if len(items) < 3 or len(items) > 4:
            print('Invalid input format')
            quit()

        sol_index, action, tag = items[:3]
        environment = items[3] if len(items) == 4 else None
        
        sol_index = int(sol_index)
        if sol_index < 0 or sol_index > len(solutions_sorted):
            print('Invalid solution selected')
            quit()
        if action not in ['b', 'd']:
            print('Invalid action')
            quit()
        if action == 'd' and environment not in ['d', 'i', 'u']:
            print('Invalid environment')
            quit()

        solution = solutions_sorted[sol_index - 1]

        if action == 'b':
            command = f'/build name={solution} tag={tag}'
        else:
            if environment == 'd': environment = 'dev'
            elif environment == 'i': environment = 'int'
            elif environment == 'u': environment = 'uat'

            command = f'\n/deploy name={solution} tag={tag} env={environment}'

        pyperclip.copy(command)
        print('Command copied to clipboard:')
        print(command)

    except Exception as e:
        print('Error: ', e)

action = 'r'
while action == 'r':
    app()
    action = input('Press "r" to run again, or any other key to exit: ')
    action = action.lower()
   
    
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

def get_environment(environment: str) -> str:
    if environment == 'd': return 'dev'
    elif environment == 'i': return 'int'
    elif environment == 'u': return 'uat'

def app(last_solution: str, last_tag: str) -> tuple[str, str] | None:

    deploy_last_tag =  f'Last solution: {last_solution} - Last tag: {last_tag}'  if last_solution != '' and last_tag != '' else ''

    with open(config_path, 'r') as f:
        solutions = json.load(f)

    solutions_sorted = sorted(solutions["solutions"])

    print('\nSolutions:')
    for index, solution in enumerate(solutions_sorted, 1):
        print(f' ({index}) {solution}')

    if deploy_last_tag != '':
        print(f' (0) {deploy_last_tag}')

    solution = input('\n .Type <solution number> [b|d] <tag> [d|i|u]\n' \
    ' .To deploy the last build, type 0 [d|i|u]\n' \
    '\n For example: 1 b my-tag d\n' \
    '> ')

    try:
        items = solution.split()
        if len(items) < 2 or len(items) > 4:
            print('Invalid input format')
            return ('', '')

        sol_index, action = items[:2]
        tag = items[2] if len(items) > 2 else None
        environment = items[3] if len(items) == 4 else None

        sol_index = int(sol_index)

        if sol_index == 0:
            solution = last_solution
            tag = last_tag
            environment = get_environment(action)
            command = f'/deploy name={solution} tag={tag} env={environment}'
        else:
            if sol_index < 0 or sol_index > len(solutions_sorted):
                print('Invalid solution selected')
                return ('', '')
            if action not in ['b', 'd']:
                print('Invalid action')
                return ('', '')
            if action == 'd' and environment not in ['d', 'i', 'u']:
                print('Invalid environment')
                return ('', '')

            solution = solutions_sorted[sol_index - 1]

            if action == 'b':
                command = f'/build name={solution} tag={tag}'
            else:
                environment = get_environment(environment)
                command = f'/deploy name={solution} tag={tag} env={environment}'

        pyperclip.copy(command)
        print('Command copied to clipboard:')
        print(command)

        return (solution, tag)

    except Exception as e:
        print('Error: ', e)

action = 'r'
last_solution = ''
last_tag = ''
while action == 'r':
    (last_solution, last_tag) = app(last_solution, last_tag)
    action = input('\nPress "r" to run again, or any other key to exit: ')
    action = action.lower()
   
    
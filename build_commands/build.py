import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "solutions.json")

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
    sol_index, action, tag, environment = solution.split()
    sol_index = int(sol_index)
    if sol_index < 0 or sol_index > len(solutions_sorted):
        print('Invalid solution selected')
        quit()
    if action not in ['b', 'd']:
        print('Invalid action')
        quit()
    if environment not in ['d', 'i', 'u']:
        print('Invalid environment')
        quit()

    solution = solutions_sorted[sol_index - 1]

    if action == 'b':
        print(f'/build name={solution} tag={tag}')
    else:
        if environment == 'd': environment = 'dev'
        elif environment == 'i': environment = 'int'
        elif environment == 'u': environment = 'uat'

        print(f'\n/deploy name={solution} tag={tag} env={environment}')
except Exception as e:
    print('Error: ', e)

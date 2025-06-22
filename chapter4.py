import random

valid_choices = ['1', '2']

def show_random_numbers():
    for _ in range(10):
        x = random.random()
        print(x)

def definitions():

    def print_lyrics():
        print("I'm a lumberjack, and I'm okay")
        print("I sleep all night and I work all day.")

    def repeat_lyrics():
        print_lyrics()
        print_lyrics()

    repeat_lyrics()

def get_choice():
    print("Functions: \n")
    print("1. ----->: show_random_numbers")
    print("2. ----->: definitions")
    print("Other key: Exit")
    choice = input("Enter your choice: ")

    return choice

def main():
    choice = get_choice()
    
    while choice in valid_choices:
        if choice == '1':
            show_random_numbers()
        elif choice == '2':
            definitions()

        print("\n")
        print("-----------------------------------------")
        choice = get_choice()
    
main()
       


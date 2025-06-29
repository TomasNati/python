import random
import sys

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

def compute_payment():
    def compute_pay(hours, rate):
        try:
            hours = float(s_hours)
            rate = float(s_rate)

            if hours > 40:
                excessHours = hours - 40
                extraPayment = excessHours * (rate * 0.5)
            else:
                extraPayment = 0
                
            totalPay = hours * rate + extraPayment

            print('The total pay is $' + str(round(totalPay, 2)))
        except:
            print('Error, please enter numeric input')

    s_hours = input('Enter the number of hours worked: ')
    s_rate = input('Enter the hourly rate: ')
    compute_pay(s_hours, s_rate)

def get_grade():
    def compute_grade(score):
        try:
            score = float(s_score)
            if score < 0 or score >= 1:
                raise ValueError("Score must be between 0 and 10")
            elif score >= 0.9:
                grade = 'A'
            elif score >= 0.8:
                grade = 'B'
            elif score >= 0.7:
                grade = 'C'
            elif score >= 0.6:
                grade = 'D'
            else:
                grade = 'F'

            print('Grade: ' + grade)
        except:
            print('Error, bad score')
    
    s_score = input('Enter the score: ')
    compute_grade(s_score)

def sumar_inputs():
    numeros_ingresados = 0
    suma = 0
    input_str = ""
    while input_str != "done":
        input_str = input("Enter a number: ")
        try:
            input_int = int(input_str)
            numeros_ingresados += 1
            suma += input_int
        except:
            print("Invalid input")
    
    print(f"Total de numeros ingresados: {numeros_ingresados}")
    print(f"Suma: {suma}")
    print(f"Promedio: {round(suma/numeros_ingresados,2)}")

def max_min_inputs():
    numeros_ingresados = 0
    suma = 0
    max = 0
    min = sys.maxsize
    input_str = ""
    while input_str != "done":
        input_str = input("Enter a number: ")
        try:
            input_int = int(input_str)
            numeros_ingresados += 1
            suma += input_int
            if input_int > max:
                max = input_int
            if input_int < min:
                min = input_int
        except:
            print("Invalid input")
    
    print(f"Total de numeros ingresados: {numeros_ingresados}")
    print(f"Suma: {suma}")
    print(f"Max number: {max}")
    print(f"Min number: {min}")

def backwards_string():
    string = input("Enter any string:")
    last_index = len(string)
    index = 1
    while index <= last_index:
        print(string[-index])
        if index < last_index:
            print("\n")
        index += 1

def count_letter_in_string():
    string = input("Enter a string: ")
    letter = input("Enter a letter to count: ")
    count = 0
    for current_letter in string:
        if current_letter == letter:
            count += 1
    print(f"The letter {letter} appear {count} times")

def count_letter_with_count():
    string = input("Enter a string: ")
    letter = input("Enter a letter to count: ")
    print(f"The letter {letter} appear {string.count(letter)} times")

valid_choices = [
    show_random_numbers, 
    definitions, 
    compute_payment, 
    get_grade, 
    sumar_inputs, 
    max_min_inputs,
    backwards_string,
    count_letter_in_string,
    count_letter_with_count
]
        
def get_choice():
    print("Functions: \n")
    print("1. ----->: show_random_numbers")
    print("2. ----->: definitions")
    print("3. ----->: compute_payment")
    print("4. ----->: get_grade")
    print("5. ----->: sumar_inputs")
    print("6. ----->: max_min_inputs")
    print("7. ----->: backwards_string")
    print("8. ----->: count_letter_in_string")
    print("9. ----->: count_letter_with_count")
    print("Other key: Exit")
    choice = input("Enter your choice: ")

    return choice

def main():
    choice = get_choice()
    try:
        choice_int = int(choice)

        while choice_int >= 0 and choice_int <= len(valid_choices):
            print(f"Executing function {choice_int}")
            method = valid_choices[choice_int -1 ]
            method()
            print("\n")
            print("-----------------------------------------")
            choice_int = int(get_choice())    

    except:
        return
    
main()
       


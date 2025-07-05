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

def print_file_to_uppercase():
    try:
        file_name = input("Enter a file name: ")
        fhand = open(file_name)
        for line in fhand:
            line = line.rstrip()
            print(line.upper())

    except:
        print("File does not exists.")

def calculate_file_confidence():
    try:
        file_name = input("Enter a file name: ")

        if file_name.lower() == "na na boo boo":
            print("NA NA BOO BOO TO YOU - You have been punk'd!")
            return
        
        fhand = open(file_name)
        number_of_values_addded = 0
        sum_of_confidences = 0
        confidence__start = "X-DSPAM-Confidence:"
        for line in fhand:
            if (line.startswith(confidence__start)):
                try:
                    separator = line.find(":")
                    confidence = float(line[separator + 1:].strip())
                    number_of_values_addded += 1
                    sum_of_confidences += confidence
                except:
                    print("Invalid format for Spam confidence line")
                    return
        
        print(f"Average confidence: {round(sum_of_confidences/number_of_values_addded, 3)}")

    except:
        print("File does not exists.")

def list_chop_and_middle():
    def chop(list_to_chop: list):
      if len(list_to_chop) == 1:
        del list_to_chop[0]
      elif len(list_to_chop) > 1:
        last_index = len(list_to_chop) - 1
        del list_to_chop[last_index]
        del list_to_chop[0]
    
    def middle(original_list: list):
      new_list = [] 
      if len(original_list) > 1:
        last_index = len(original_list) - 1
        new_list = original_list[1:last_index]
      return new_list
    
    list_sample = []
    copy_list = list_sample[:]
    middle_l = middle(list_sample)
    chop(list_sample)
    print(f"List: {copy_list} - Chop 0: {list_sample} - Middle 0: {middle_l}")

    list_sample = [45]
    copy_list = list_sample[:]
    middle_l = middle(list_sample)
    chop(list_sample)
    print(f"List: {copy_list} - Chop 1: {list_sample} - Middle 1: {middle_l}")

    list_sample = [9, 12, 465, 8]
    copy_list = list_sample[:]
    middle_l = middle(list_sample)
    chop(list_sample)
    print(f"List: {copy_list} - Chop 4: {list_sample} - Middle 4: {middle_l}")

    list_sample = [1,2,3,4,5,6,7,8,9.0]
    copy_list = list_sample[:]
    middle_l = middle(list_sample)
    chop(list_sample)
    print(f"List: {copy_list} - Chop 4: {list_sample} - Middle 4: {middle_l}")
    
def print_from_lines():
    try:
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)    
        for line in fhandle:
            words = line.split()
            if len(words) < 3 or words[0] != "From" : continue
            print(words[2])    
    except Exception as e:
        print("An error occurred:", e)

valid_choices = [
    show_random_numbers, 
    definitions, 
    compute_payment, 
    get_grade, 
    sumar_inputs, 
    max_min_inputs,
    backwards_string,
    count_letter_in_string,
    count_letter_with_count,
    print_file_to_uppercase,
    calculate_file_confidence,
    list_chop_and_middle,
    print_from_lines
]
        
def get_choice():
    print("Functions: \n")
    print("1.  ----->: show_random_numbers")
    print("2.  ----->: definitions")
    print("3.  ----->: compute_payment")
    print("4.  ----->: get_grade")
    print("5.  ----->: sumar_inputs")
    print("6.  ----->: max_min_inputs")
    print("7.  ----->: backwards_string")
    print("8.  ----->: count_letter_in_string")
    print("9.  ----->: count_letter_with_count")
    print("10. -----> print_file_to_uppercase")
    print("11. -----> calculate_file_confidence")
    print("12. -----> list_chop_and_middle")
    print("13. -----> print_from_lines")
    print("Other key: Exit")
    choice = input("Enter your choice: ")

    return choice

def main():
    choice = get_choice()
    try:
        choice_int = int(choice)

        while choice_int >= 0 and choice_int <= len(valid_choices):
            method = valid_choices[choice_int -1 ]
            method()
            print("\n")
            print("-----------------------------------------")
            choice_int = int(get_choice())    

    except Exception as e:
        print("An error occurred:", e)
        return
    
main()
       

import random

valid_choices = ['1', '2', '3', '4']

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

        
def get_choice():
    print("Functions: \n")
    print("1. ----->: show_random_numbers")
    print("2. ----->: definitions")
    print("3. ----->: compute_payment")
    print("4. ----->: get_grade")
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
        elif choice == '3':
            compute_payment()
        elif choice == '4':
            get_grade()

        print("\n")
        print("-----------------------------------------")
        choice = get_choice()
    
main()
       


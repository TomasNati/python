import random
import sys
import re
import socket

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

def find_and_sort_unique_words():
    try:
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)    
        unique_words = []
        for line in fhandle:
            words = line.split()
            for word in words:
                if not word in unique_words:
                    unique_words.append(word)

        unique_words.sort()
        print(unique_words)

    except Exception as e:
        print("An error occurred:", e)

def count_mbox_froms():
    try:
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)    
        count = 0
        for line in fhandle:
            words = line.split()
            if len(words) < 2 or words[0] != "From" : continue
            sender = words[1]
            count += 1
            print(sender)

        print(f"There were {count} lines in the file with From as the first word") 

    except Exception as e:
        print("An error occurred:", e)

def max_min_inputs_improved():
    numeros = []
    input_str = ""
    while input_str != "done":
        input_str = input("Enter a number: ")
        try:
            input_int = int(input_str)
            numeros.append(input_int)
        except:
            print("Invalid input")
    
    print(f"Total de numeros ingresados: {len(numeros)}")
    print(f"Max number: {max(numeros)}")
    print(f"Min number: {min(numeros)}")

def create_dict_from_words():
    try:
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)    
        my_words = dict()
        for line in fhandle:
            words = line.split()
            for word in words:
                if not word in my_words:
                    my_words[word] = 1

        print(f"There were {len(my_words)} words in the file") 

    except Exception as e:
        print("An error occurred:", e)

def count_days_of_emails():
    try:
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)    
        days = dict()
        for line in fhandle:
            words = line.split()
            if len(words) < 3 or words[0] != "From": continue
            current_day = words[2]
            days[current_day] = days.get(current_day, 0) + 1
        print(days)
    except Exception as e:
        print("An error occurred:", e)

def count_senders_of_emails():
    try:
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)
        senders = dict()
        for line in fhandle:
            words = line.split()
            if len(words) < 2 or words[0] != "From": continue
            sender = words[1]
            senders[sender] = senders.get(sender, 0) + 1
        
        print("Senders: ", senders)
        print("\n")
        max_sender = ""
        max_sent = 0
        for sender in senders:
            if senders[sender] > max_sent:
                max_sender = sender
                max_sent = senders[sender]
        print(f"{max_sender} has sent the most emails: {max_sent}")

    except Exception as e:
        print("An error has ocurred:", e)

def count_domains_of_emails():
    try:
        file_name = input("Enter a file name: " )
        fhandle = open(file_name)
        domains = dict()
        for line in fhandle:
            words = line.split()
            if len(words) < 2 or words[0] != "From": continue
            sender = words[1]
            parts = sender.split("@")
            if len(parts) != 2: continue
            domain = parts[1]
            domains[domain] = domains.get(domain, 0) + 1
        print(domains)

    except Exception as e:
        print("An error has occured: ", e)

def count_senders_of_emails_with_tuple():
    try:
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)
        senders = dict()
        for line in fhandle:
            words = line.split()
            if len(words) < 2 or words[0] != "From": continue
            sender = words[1]
            senders[sender] = senders.get(sender, 0) + 1
        
        print("Senders: ", senders)
        print("\n")
       
        senders_list = []
        for sender_email, emails_sent in senders.items():
            senders_list.append((emails_sent, sender_email))
        
        senders_list.sort(reverse=True)
        emails_sent, sender_email = senders_list[0]
        print(f"The sender with email {sender_email} sent the most emails: {emails_sent}")

    except Exception as e:
        print("An error has ocurred:", e)

def count_hours_dist_in_emails():
    try:
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)
        emails_per_hour = dict()
        
        for line in fhandle:
            words = line.split()
            if len(words) < 6 or words[0] != "From": continue
            hour_string = words[5]
            hour, _, _ = hour_string.split(":")
            emails_per_hour[hour] = emails_per_hour.get(hour, 0) + 1 
        
        hours_dist = list()
        for email_hour, emails in emails_per_hour.items():
            hours_dist.append((email_hour, emails))
        
        hours_dist.sort()
        for hour, emails in hours_dist:
            print(f"{hour}: {emails}")


    except Exception as e:
        print("An error has ocurred: ", e)

def count_letter_frequency():
    a_ord = ord('a')
    z_ord = ord('z')

    try:
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)

        letters_frequency = dict()

        for line in fhandle:
            for letter in line:
                letter_lower = letter.lower()
                letter_ord = ord(letter_lower)
                if a_ord <= letter_ord and letter_ord <= z_ord:
                    letters_frequency[letter_lower] = letters_frequency.get(letter_lower, 0) + 1
        
        letters_dist = list()
        for letter, count in letters_frequency.items():
            letters_dist.append((count, letter))
        
        letters_dist.sort(reverse=True)
        for count, letter in letters_dist:
            print(f"{letter}: {count}")

    except Exception as e:
        print("An error has ocurred: ", e)

def count_expression_in_file():
    try:
        reg_ex = input("Enter a regular expression: ")
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)
        count = 0
        for line in fhandle:
            if re.search(reg_ex, line):
                count += 1
        print(f"{file_name} has {count} lines that match the expression {reg_ex}")

    except Exception as e:
        print("An error has occured: ", e)

def find_average_of_revision():
    try:
        reg_ex = '^New Revision: ([0-9]+)$'
        file_name = input("Enter a file name: ")
        fhandle = open(file_name)
        revisions = []
        for line in fhandle:
            matches =  re.findall(reg_ex, line)
            if len(matches) == 1:
                revisions.append(int(matches[0]))

        average =round(sum(revisions)/len(revisions),2)
        print(f"The average is: {average}")

    except Exception as e:
        print("An error has occured: ", e)

def sockets_1():
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysock.connect(('data.pr4e.org', 80))
    cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode()
    mysock.send(cmd)

    while True:
        data = mysock.recv(512)
        if len(data) < 1:
            break
        print(data.decode(),end='')
    
    mysock.close()

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
    print_from_lines,
    find_and_sort_unique_words,
    count_mbox_froms,
    max_min_inputs_improved,
    create_dict_from_words,
    count_days_of_emails,
    count_senders_of_emails,
    count_domains_of_emails,
    count_senders_of_emails_with_tuple,
    count_hours_dist_in_emails,
    count_letter_frequency,
    count_expression_in_file,
    find_average_of_revision,
    sockets_1
]
        
def get_choice():
    print("Functions: \n")
    for index, my_function in enumerate(valid_choices):
        print(f"{index + 1}. ------->: {my_function.__name__}")
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
       

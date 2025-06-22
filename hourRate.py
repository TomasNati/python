s_hours = input('Enter the number of hours worked: ')
s_rate = input('Enter the hourly rate: ')
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


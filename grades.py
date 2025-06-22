s_score = input('Enter the score: ')
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
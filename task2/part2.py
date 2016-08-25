string_default=["abrakakarba"]

try:
    print("Leave empty for default")
    string_in=input()
    if not string_in:
        raise ValueError()
except ValueError:
    string_in=string_default

def checks(stringa):
    check=(stringa==stringa[::-1])
    if check:
        print("the word "+str(stringa)+" is a palindrome")
    else:
        print("the word "+str(stringa)+" is not a palindrome")

checks(string_in)
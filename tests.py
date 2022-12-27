from Dependencies.csvcode import Csvcode
csv = Csvcode('demo')
same = False
while not(same):
    passwordA = ''
    passwordB = ''
    passwordA = input('\nPlease enter a password for this universe:')
    passwordB = input('Please it again to confirm:')
    same = passwordB == passwordA
    if not(same):
        print('\nThose passwords did not match, Please try again')

print(csv.passwordhash(passwordA))

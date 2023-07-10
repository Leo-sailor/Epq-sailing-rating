# imports
from datetime import datetime, date, timedelta
from Framework.text_ui import valid_nat

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def getfieldnumber(resulttype: str) -> int:
    try:
        resulttype.lower()
    except AttributeError:
        pass
    match resulttype:
        case 'n' | 'name':
            findtypeloc = -1  # makes sure the next bit will be bypassed
        case 'sail number' | 's' | 'sail':
            findtypeloc = 2  # the column location of the data
        case 'champ number' | 'championship number' | 'c' | 'champ':
            findtypeloc = 1
        case 'region' | 'z':
            findtypeloc = 5
        case 'nat' | 'nation' | 'nationality' | 't':
            findtypeloc = 6
        case 'l' | 'light wind rating' | 7:
            findtypeloc = 7
        case 'medium wind rating' | 'm' | 8:
            findtypeloc = 8
        case 'high wind rating' | 'h' | 9:
            findtypeloc = 9
        case 'ranking' | 'r':
            findtypeloc = 11
        case 'overall rating' | 'o' | 10:
            findtypeloc = 10
        case 'events completed' | 'e':
            findtypeloc = 12
        case 'date of last event' | 'd':
            findtypeloc = 13
        case '14' | 'a' | 'all':
            findtypeloc = -2  # bypasses next stage
        case _:
            findtypeloc = 0
    return findtypeloc


def two_thousand_to_datetime(days: int) -> date:
    thousand = date(2000, 1, 1)
    delta = timedelta(days)
    return thousand + delta


def days_since_two_thousand(in_date: date | datetime = None) -> int:
    thousand = date(2000, 1, 1)
    if in_date is None:
        now = date.today()
    else:
        now = in_date
    day = now - thousand
    return day.days


def generate_sailor_id(ui, nat: str | None, sailno: str | int, first: str, surname: str) -> tuple[str, str]:
    """
    This function generates a sailorid from its components
    :param nat: 3 letter sting or none
    :param sailno: 5 number string
    :param first: string
    :param surname: string
    :param ui:
    :return: string
    """
    iden = ''
    if nat is None:
        nat = ui.g_nat(f'of {first} {surname}')
    nat = nat.upper()
    if nat not in valid_nat:
        nat = ui.g_nat(f'of {first} {surname}')
    first += '000'
    surname += '000'
    sailno = str(sailno)
    newsailno = '0000' + sailno
    if newsailno[-2:] == '.0':
        newsailno = sailno[:-2]
    iden += nat[:2]
    iden += '-'
    iden += newsailno[-4:]
    iden += '-'
    iden += first[:3]
    iden += surname[:2]
    return iden.lower(), nat


def csv_line_generate(sailorid: str, nat: str, sailno: str, first: str, surname: str, region: str,
                      champnum: str) -> str:
    """
    This function generates a csv line from its components ready to be appended to a csv
    :param sailorid: sailorid
    :param nat: 3 letter sting
    :param sailno: 5 number string
    :param first: string
    :param surname: string
    :param region: 2 letter number string or ''
    :param champnum: 3 number stinf or ''
    :return:
    """
    rank = 0

    first.lower()
    surname.lower()
    region = region[:3].upper().strip()
    champnum = '000' + str(champnum)
    champnum = champnum[-3:]
    if nat not in valid_nat:
        nat.upper()
        nat.strip()

    parts = [sailorid, champnum, sailno, first, surname, region, nat, 1500, 1500, 1500, 1500, rank,
             days_since_two_thousand()]

    line = ','.join(parts)

    # print('{}'.format(line))

    return line


def text_blocks(amount):
    """
    This function prints a help message
    :param amount: the type of help messages to be printed
    :return: prints the help
    """
    if amount == 0:
        # List of instructions for the user
        print('1 - view a sailor'
              '\n2 - ')
    elif amount == 1:
        # Detailed instructions
        print('\nDetailed instructions and more details')
        print('(1) to add a new event')
        print('(2) to add a new sailor')
        print('(3) to get a sailors information')
        print('(4) to quit')
        print('(5) to get sailor info over time')
        print('(6) to print the universe')
        print('(7) to exit the universe')
        print('(8) to import sailors')
        print('(9) to graph sailors over time')
    elif amount == 2:
        # developer instructions with methods locations objects and modes and other parameters and explainations
        print('\nclass: General method: help parameters: mode explaination: if the mode is 0 basic instructions '
              'will be printed, if its 1 detailed instructions will be printed, if its 2 developer '
              'instructions will be printed')
        print('class: General method: multiindex parameters: list(list), term(str or int) explaination: will return'
              ' the index of all the ocourances  of the term inside of the input list')
        print('class: General method: Rank sailor parameters: ratings(list) explaination: will take a list of '
              'ratings and sort them from high to low ')
        print('class: General method: generaterank parameters: rating(int) ratings(list) '
              'explaination: will find the rank of the rating in the unsorted list ratings')
        print('class: General method: __firstcap parameters: word(string) explaination: first letter to a capital')
        print('class: General method: Csvlinegenerate Parameters')


if __name__ == '__main__':
    exit()

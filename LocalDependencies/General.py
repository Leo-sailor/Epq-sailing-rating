# imports
from datetime import datetime, date, timedelta
from LocalDependencies.Framework.text_ui import valid_nat

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def get_field_number(result_type: str) -> int:
    try:
        result_type.lower()
    except AttributeError:
        pass
    match result_type:
        case 'n' | 'name':
            find_type_loc = -1  # makes sure the next bit will be bypassed
        case 'sail number' | 's' | 'sail':
            find_type_loc = 2  # the column location of the data
        case 'champ number' | 'championship number' | 'c' | 'champ':
            find_type_loc = 1
        case 'region' | 'z':
            find_type_loc = 5
        case 'nat' | 'nation' | 'nationality' | 't':
            find_type_loc = 6
        case 'l' | 'light wind rating' | 7:
            find_type_loc = 7
        case 'medium wind rating' | 'm' | 8:
            find_type_loc = 8
        case 'high wind rating' | 'h' | 9:
            find_type_loc = 9
        case 'ranking' | 'r':
            find_type_loc = 11
        case 'overall rating' | 'o' | 10:
            find_type_loc = 10
        case 'events completed' | 'e':
            find_type_loc = 12
        case 'date of last event' | 'd':
            find_type_loc = 13
        case '14' | 'a' | 'all':
            find_type_loc = -2  # bypasses next stage
        case _:
            find_type_loc = 0
    return find_type_loc


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
    identity = ''
    if nat is None:
        nat = ui.g_nat(f'of {first} {surname}')
    nat = nat.upper()
    if nat not in valid_nat:
        nat = ui.g_nat(f'of {first} {surname}')
    first += '000'
    surname += '000'
    sailno = str(sailno)
    new_sailno = '0000' + sailno
    if new_sailno[-2:] == '.0':
        new_sailno = sailno[:-2]
    identity += nat[:2]
    identity += '-'
    identity += new_sailno[-4:]
    identity += '-'
    identity += first[:3]
    identity += surname[:2]
    return identity.lower(), nat


def csv_line_generate(sailorid: str, nat: str, sailno: str, first: str, surname: str, region: str,
                      champ_num: str) -> str:
    """
    This function generates a csv line from its components ready to be appended to a csv
    :param sailorid: sailorid
    :param nat: 3 letter sting
    :param sailno: 5 number string
    :param first: string
    :param surname: string
    :param region: 2 letter number string or ''
    :param champ_num: 3 number string or ''
    :return:
    """
    rank = 0

    first.lower()
    surname.lower()
    region = region[:3].upper().strip()
    champ_num = '000' + str(champ_num)
    champ_num = champ_num[-3:]
    if nat not in valid_nat:
        nat.upper()
        nat.strip()

    parts = [sailorid, champ_num, sailno, first, surname, region, nat, 1500, 1500, 1500, 1500, rank,
             days_since_two_thousand()]
    line = ','.join(parts)
    return line

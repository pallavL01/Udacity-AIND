from solution import *
from solution_test import *

values = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
          'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
          'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
          'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
          'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
          'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
          'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
          'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
          'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
          'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
          'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}    
#display(values)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    while(True):
        copy_values = values.copy()
        for unit in unitlist:
            #print(unit)
            naked_twin = [x for x in unit for y in unit if (len(values[x]) == 2) and (values[x] == values[y]) and x != y]
            if naked_twin != []:
                # Digits which need to be replaced in the unit because of naked twin
                digits = values[naked_twin[0]]
                #print(digits)
                # For every box in the unit, if any of the digits appear in the values[box], replace the value with ''
                for digit in digits:
                    for box in unit:
                        a = values[box]
                        if digit in a and box not in naked_twin:
                            values[box] = values[box].replace(digit, '')   

        if all([values[x] == copy_values[x] for x in boxes]):
            break                          

    return values       

after_naked_twin = naked_twins(values)
print(display(after_naked_twin))    


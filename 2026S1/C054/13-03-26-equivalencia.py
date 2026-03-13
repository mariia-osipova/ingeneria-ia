def function(x: bool, y: bool):
    if x == True and y == False:
        if x == True or y == False:
            return 'Op.1'
        else:
            if x == True and (x == True or y == False):
                return 'Op.2'
            else:
                if x == False and y == False:
                    return 'Op.3'
    else:
        if x == False or y == True:
            return 'Op.4'
        else:
            if x == True and (x == True or y == False):
                return 'Op.5'
            else:
                if x == False and y == False:
                    return 'Op.6'

def function_the_best(x:bool, y:bool):
    if x and not y:
        return 'Op.1'
    elif not x or y:
        return 'Op.4'

def main():
    print('result of (1,0) is', function(True, False), 'for the 1st func and', function_the_best(True, False))
    print('result of (1, 1) is', function(True, True), 'for the 1st func and', function_the_best(True, True))
    print('result of (0, 0) is', function(False, False), 'for the 1st func and', function_the_best(False, False))
    print('result of (0, 1) is', function(False, True), 'for the 1st func and', function_the_best(False, True))

main()
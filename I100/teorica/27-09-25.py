people = eval(input())

def print_names2(people):
    """Print a list of people's names, which each person's name
       is itself a list of names (first name, second name etc)
    """

    index_last = len(people)
    i = 0
    j = 0

    while index_last != 0:
        print(*people[i])
        i += 1
        index_last -= 1

    return True

print_names2(people)
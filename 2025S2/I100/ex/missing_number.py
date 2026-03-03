

def missing_number(n, s):
    s = sorted(s)
    i = 0
    list_r = [i + 1 for i in range(n)]
    for j in range(len(list_r)):
        if list_r[j] not in list:
            mis_num = list_r[j]

    return mis_num

def str_to_list(list):
    return list(map(int, s.split()))

def main():
    n = int(input())
    list = input()
    list = str_to_list(list)
    mis_num = missing_number(n, list)
    print(mis_num)

if __name__ == '__main__':
    main()
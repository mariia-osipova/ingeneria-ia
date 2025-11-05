def weird_algorythm(n):
    if n < 0:
        raise ValueError('n must be greater than 0')
    list_n = [n]
    while n != 1:
        if n % 2 == 0:
            n = n / 2
            list_n.append(int(n))
        else:
            n = 3 * n + 1
            list_n.append(int(n))
    return list_n

def main():
    n = int(input())
    list_n = weird_algorythm(n)
    print(" ".join(map(str, list_n)))
    # double = map(lambda x: x * 2, list_n)
    # print(" ".join(map(str, double)))

if __name__ == '__main__':
    main()

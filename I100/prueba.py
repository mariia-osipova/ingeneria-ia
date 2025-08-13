from math import gcd

# print("print a")
# (a) = int(input())
#
# print("print b")
# (b) = int(input())
#
# def euclidian(a,b):
#     if b==0:
#         return a
#     else:
#         return euclidian(b,a%b)
#
# print(euclidian(a,b))

print("print a")
(a) = int(input())

print("print b")
(b) = int(input())

print("print c")
(c) = int(input())

def euclidian(a,b):
    if b==0:
        return a
    else:
        return euclidian(b,a%b)

d = euclidian(a,b)
print(d)

if c == 0 or c % d != 0:
    print("impossible")

a = int(a / d)
b = int(b / d)
c = int(c / d)

print(a,"x+",b,"y=", c, sep="")
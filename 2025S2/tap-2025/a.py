 #tap = subsequence

# s = input()
#
# for k in range(len(s)):
#     for j in range(k):
#         for i in range(j):
#             if s[i] + s[j] + s[k] == "TAP":
#                 print("S")
#                 exit()
# print("N")


s = input()
target = "TAP"
# i en s
# j en target
def subseq(i, j):
    if j == len(target):
        return True
    for pos in range(i, len(s)):
        if s[pos] == target[j]:
            if subseq(pos + 1, j + 1):
                return True

    return False

if subseq(0, 0): #
    print("S")
else:
    print("N")

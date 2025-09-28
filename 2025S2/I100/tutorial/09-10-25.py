password = "hellobitch"

def login():
    pas = input()
    if pas == password:
        print("Login Successful")
    else:
        i = 1
        while i < 3:
            if pas != password:
                i += 1
                print("Try Again")
                pas = input()
            else:
                print("Login Successful")
                break
        print("fck")

login()





n = 5

def repeated_entry(vector):
    set_ = set()
    for i in range(len(vector)):
        set_.add(vector[i])
    if len(set_) == len(vector):
        return 0
    else:
        return 1

def activation_check(serial_code):
    entries = serial_code.split("-")
    if len(entries) != n:
        return 2

    matrix = [[0]*n for _ in range(n)]

    for i in range(n):
        if len(entries[i]) != n:
            return 2
        for j in range(n):
            if entries[i][j] < '1' or entries[i][j] > str(n):
                return 2
            matrix[i][j] = entries[i][j]
    
    for i in range(n):
        vector = [matrix[i][j] for j in range(n)]
        if repeated_entry(vector):
            return 0

    for j in range(n):
        vector = [matrix[i][j] for i in range(n)]
        if repeated_entry(vector):
            return 0

    vector = [matrix[i][i] for i in range(n)]
    if repeated_entry(vector):
        return 0

    vector = [matrix[i][n-1-i] for i in range(n)]
    if repeated_entry(vector):
        return 0

    sum__ =  0
    for i in range(n):
        for j in range(n):
            sum__ += int(matrix[i][j])
    
    if not (sum__ % 96 == 75):
        return 0

    return 1

if __name__ == '__main__':
    print("""██╗  ██╗██╗   ██╗██╗   ██╗██████╗  ██████╗ ███████╗
██║ ██╔╝██║   ██║██║   ██║██╔══██╗██╔═══██╗██╔════╝
█████╔╝ ██║   ██║██║   ██║██║  ██║██║   ██║███████╗
██╔═██╗ ██║   ██║██║   ██║██║  ██║██║   ██║╚════██║
██║  ██╗╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝
                                                   
    """)
    serial_code = input("Input your activation code: ")

    result = activation_check(serial_code)
    print()
    if result > 1:
        print("Your serial has an incorrect format, look at the back of your CD.\n")
    elif result:
        with open("flag", "r") as f:
            flag = f.read()
            print(flag)
    else:
        print("Stop trying, buy the license :)\n")
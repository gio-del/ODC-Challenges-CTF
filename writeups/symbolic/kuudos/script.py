from z3 import *
import time

n = 5

## Return Must Be 1: key like this xyzwk-xyzwk-xyzwk-xyzwk-xyzwk

s = Solver()

key = [[Int("key_%d_%d" % (i,j)) for i in range(n)] for j in range(n)]

# Only numbers in [1, 5]
for i in range(n):
    for j in range(n):
        s.add(key[i][j] >= 1, key[i][j] <= 5)

# No reapeted on each column
for j in range(n):
    distinct = [key[i][j] for i in range(n)]
    s.add(Distinct(distinct))

# No repeated on each row
for i in range(n):
    distinct = [key[i][j] for j in range(n)]
    s.add(Distinct(distinct))

# No repeated on diagonal
s.add(Distinct([key[i][i] for i in range(n)]))

# No repeated on the other diagonal
s.add(Distinct([key[i][n-i-1] for i in range(n)]))

# Sum % 96 == 75
_sum = 0
for i in range(n):
    for j in range(n):
        _sum += key[i][j]
s.add(_sum % 96 == 75)

print(s.check())
m = s.model()
# print(m)

key_str = ''
for i in range(n):
    for j in range(n):
        key_str += "" + m[key[i][j]].as_string()
    if(i != n-1):    
        key_str += '-'

print('Key:', key_str)

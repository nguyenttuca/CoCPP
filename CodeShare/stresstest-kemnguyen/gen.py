from random import *

out = open("bai3.inp", "w")

n = randint(1, 1000)
out.write(str(n) + "\n")

for _ in range(n):
    out.write(str(randint(1, 1000000)) + " ")
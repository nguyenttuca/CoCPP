from subprocess import *

q = 5
while q > 0:
	run(["python3", "gen.py"])

	inp = open("bai3.inp", "r")
	out = open("bai3.ans", "w")
	run(["python3", "trau.py"], stdin=inp, stdout=out, stderr=DEVNULL)
	inp.close()
	out.close()

	inp = open("bai3.inp", "r")
	out = open("bai3.out", "w")
	run(["python3", "chuan.py"], stdin=inp, stdout=out, stderr=DEVNULL)
	inp.close()
	out.close()

	inp1 = open("bai3.out", "r")
	inp2 = open("bai3.ans", "r")

	a1 = list(map(int, inp1.read().split()))
	a2 = list(map(int, inp2.read().split()))

	if a1 == a2:
		print("AC")
	else:
		print("WA")
		break

	inp1.close()
	inp2.close()

	q -= 1
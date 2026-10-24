import random
import time
from railfence import norm
from columnar import encrypt
from break_columnar import attack, descifrar

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NCOLS = [4, 5, 6, 7]
NS = [60, 120, 200]
TRIALS = 50

text = norm(open("data/text.txt").read())
random.seed(1)

clave = "".join(random.sample(abc, 5))
claro = text[:60]
orden = tuple(sorted(range(5), key=lambda i: clave[i]))
print("convencion correcta:", descifrar(encrypt(claro, clave, "X"), orden) == claro)

print("\nproporcion de txt recuperados")
print("cols \\ n | " + " | ".join("%5d" % n for n in NS))
for k in NCOLS:
    fila = []
    for n in NS:
        bien = 0
        for _ in range(TRIALS):
            i = random.randint(0, len(text) - n)
            claro = text[i:i + n]
            clave = "".join(random.sample(abc, k))
            cifrado = encrypt(claro, clave, "X")
            esperado = claro + "X" * (-len(claro) % k)
            if attack(cifrado, k)[1] == esperado:
                bien += 1
        fila.append(100 * bien / TRIALS)
    print("%8d | " % k + " | ".join("%4.0f%%" % f for f in fila))

print("\ntiempo de una llamada a attack")
for k in range(4, 10):
    cifrado = encrypt(text[:200], "".join(random.sample(abc, k)), "X")
    t0 = time.time()
    attack(cifrado, k)
    t = time.time() - t0
    print("n_cols = %d: %.2f s" % (k, t))
    if t > 10:
        break

#   Execute
#   python -m tests.break_columnar_test
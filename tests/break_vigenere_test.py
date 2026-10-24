import random
from railfence import norm
from practice1_copy.vigenere import encrypt_vigenere
from keylength import find_key_length
from break_vigenere import attack

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KS = [3, 5, 7, 9]
NS = [100, 150, 200, 300, 400]
TRIALS = 100

text = norm(open("data/text.txt").read())

random.seed(1)
completa = {}
longitud = {}
for k in KS:
    for n in NS:
        bien_clave = 0
        bien_long = 0
        for hh in range(TRIALS):
            i = random.randint(0, len(text) - n)
            claro = text[i:i + n]
            clave = "".join(random.choice(abc) for _ in range(k))
            cifrado = encrypt_vigenere(claro, clave)
            if find_key_length(cifrado) == k:
                bien_long = bien_long + 1
            if attack(cifrado)[0] == clave:
                bien_clave = bien_clave + 1
        completa[(k, n)] = 100 * bien_clave / TRIALS
        longitud[(k, n)] = 100 * bien_long / TRIALS


def imprimir(titulo, tabla):
    print("\n" + titulo)
    print("  k \\ n | " + " | ".join("%5d" % n for n in NS))
    for k in KS:
        print("%7d | " % k + " | ".join("%4.0f%%" % tabla[(k, n)] for n in NS))


imprimir("Table 1: complete key recovered", completa)
imprimir("Table 2: key length correct", longitud)

#   Execute
#   python -m tests.break_vigenere_test
import math
from itertools import permutations
from railfence import norm

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
corpus = open("data/alicew.txt").read()


def tabla_bigramas(txt):
    texto = norm(txt)
    cuenta = [[1] * 26 for _ in range(26)]
    for a, b in zip(texto, texto[1:]):
        cuenta[abc.index(a)][abc.index(b)] += 1
    tabla = []
    for fila in cuenta:
        total = sum(fila)
        tabla.append([math.log(c / total) for c in fila])
    return tabla


LOGP = tabla_bigramas(corpus)


def puntuar(texto):
    nums = [abc.index(c) for c in texto]
    total = 0.0
    for a, b in zip(nums, nums[1:]):
        total += LOGP[a][b]
    return total


def descifrar(cifrado, orden):
    n = len(orden)
    filas = len(cifrado) // n
    columnas = [None] * n
    for j in range(n):
        columnas[orden[j]] = cifrado[j * filas:(j + 1) * filas]
    texto = ""
    for r in range(filas):
        for c in range(n):
            texto += columnas[c][r]
    return texto


def attack(ciphertext: str, n_cols: int, language: str = "en") -> tuple[tuple[int, ...], str]:
    texto = norm(ciphertext)
    mejor_orden = None
    mejor_texto = ""
    mejor_punt = float("-inf")
    for orden in permutations(range(n_cols)):
        candidato = descifrar(texto, orden)
        p = puntuar(candidato)
        if p > mejor_punt:
            mejor_punt = p
            mejor_orden = orden
            mejor_texto = candidato
    return mejor_orden, mejor_texto

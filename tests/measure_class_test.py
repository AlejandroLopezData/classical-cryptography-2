import random
import measure
from columnar import encrypt
from railfence import norm
from freq import LETTER_FREQUENCIES
from practice1_copy.monoalpha import encrypt_mono, alphabet

tabla = LETTER_FREQUENCIES["en"]
abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
pesos = [tabla[c.lower()] for c in abc]
LARGOS = [60, 120, 250, 400]
N = 150

text = norm(open("data/text.txt").read())
assert len(text) >= 700, "el texto de referencia es demasiado corto"


def muestra(largo, es_trans, pad):
    i = random.randint(0, len(text) - largo)
    t = text[i:i + largo]
    if es_trans:
        clave = "".join(random.sample(abc, random.randint(4, 10)))
        if pad == "azar":
            while len(t) % len(clave) != 0:
                t = t + random.choices(abc, pesos)[0]
        return encrypt(t, clave, "X")
    clave = "".join(random.sample(alphabet, len(alphabet)))
    return encrypt_mono(t, clave)


def calibrar(pad):
    datos = [(measure.chi_squared(muestra(l, t, pad), tabla), t)
             for l in LARGOS for _ in range(N) for t in (True, False)]
    mejor = min(range(1, 400),
                key=lambda i: sum((v < i / 100) != t for v, t in datos))
    measure.umbral = mejor / 100


def error(largo, es_trans, pad):
    esperado = "transposition" if es_trans else "substitution"
    mal = sum(measure.classify(muestra(largo, es_trans, pad)) != esperado
              for _ in range(N))
    return 100 * mal / N


def medir(pad):
    calibrar(pad)
    filas = []
    for largo in LARGOS:
        filas.append((error(largo, True, pad), error(largo, False, pad)))
    return measure.umbral, filas


random.seed(1)
print("letras del texto:", len(text))
ux, fx = medir("X")
ua, fa = medir("azar")
print("umbral X:", ux, "| umbral azar:", ua)
print("      |        pad X         |      pad azar")
print(" leng | transp. error | sust. error | transp. error | sust. error")
for i in range(len(LARGOS)):
    print("%5d | %12.1f%% | %10.1f%% | %12.1f%% | %10.1f%%" %
          (LARGOS[i], fx[i][0], fx[i][1], fa[i][0], fa[i][1]))


# para responder pregunta 3 test
measure.umbral = ux

suma = sum(tabla.values())
fx = tabla["x"] / suma
n = 66
pad = 6
esperado = n * fx
aporte = (pad - esperado) ** 2 / esperado

print("\n--- aporte del relleno (66 letras, 6 X) ---")
print("frecuencia de X:", fx)
print("esperado de X en 66 letras: %.4f" % esperado)
print("aporte de las 6 X (formula): %.2f | por letra (/66): %.3f" % (aporte, aporte / n))

claro = text[:60]
sin = measure.chi_squared(claro, tabla)
con = measure.chi_squared(claro + "X" * pad, tabla)

print("chi_squared sin relleno (60 letras): %.3f" % sin)
print("chi_squared con 6 X (66 letras):     %.3f" % con)
print("diferencia (lo que aporta el relleno): %.3f" % (con - sin))
print("umbral (relleno X):", measure.umbral)
print("clasificacion sin relleno:", measure.classify(claro))
print("clasificacion con 6 X:    ", measure.classify(claro + "X" * pad))


#   Execute
#   python -m pytest tests/measure_class_test.py
#   python -m tests.measure_class_test


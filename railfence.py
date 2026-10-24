
def norm(t):
    res = ""
    for c in t.upper():
        if c >= "A" and c <= "Z":
            res = res + c
    return res


def patron(n, rails):
    filas = []
    fila = 0
    paso = 1
    for i in range(n):
        filas.append(fila)
        if fila == 0:
            paso = 1
        if fila == rails - 1:
            paso = -1
        fila = fila + paso
    return filas


def encrypt(plaintext: str, rails: int) -> str:
    texto = norm(plaintext)
    p = patron(len(texto), rails)
    res = ""
    for r in range(rails):
        for i in range(len(texto)):
            if p[i] == r:
                res = res + texto[i]
    return res


def decrypt(ciphertext: str, rails: int) -> str:
    texto = norm(ciphertext)
    p = patron(len(texto), rails)
    res = list(texto)
    k = 0
    for r in range(rails):
        for i in range(len(texto)):
            if p[i] == r:
                res[i] = texto[k]
                k = k + 1
    return "".join(res)



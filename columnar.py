from railfence import norm


def key_order(keyword: str) -> list[int]:
    clave = norm(keyword)
    orden = []
    for i in range(len(clave)):
        pos = 1
        for j in range(len(clave)):
            if clave[j] < clave[i] or (clave[j] == clave[i] and j < i):
                pos = pos + 1
        orden.append(pos)
    return orden


def encrypt(plaintext: str, keyword: str, pad: str = "X") -> str:
    texto = norm(plaintext)
    orden = key_order(keyword)
    ancho = len(orden)
    while len(texto) % ancho != 0:
        texto = texto + pad
    res = ""
    for n in range(1, ancho + 1):
        colum = orden.index(n)
        for i in range(colum, len(texto), ancho):
            res = res + texto[i]
    return res


def decrypt(ciphertext: str, keyword: str) -> str:
    texto = norm(ciphertext)
    orden = key_order(keyword)
    ancho = len(orden)
    filas = len(texto) // ancho
    res = list(texto)
    k = 0
    for n in range(1, ancho + 1):
        colum = orden.index(n)
        for f in range(filas):
            res[f * ancho + colum] = texto[k]
            k = k + 1
    return "".join(res)


def encrypt_double(plaintext: str, kw1: str, kw2: str, pad: str = "X") -> str:
    primero = encrypt(plaintext, kw1, pad)
    return encrypt(primero, kw2, pad)


def decrypt_double(ciphertext: str, kw1: str, kw2: str) -> str:
    paso = decrypt(ciphertext, kw2)
    ancho = len(key_order(kw1))
    largo = len(paso) - len(paso) % ancho
    return decrypt(paso[:largo], kw1)


from railfence import norm


def repeats(ciphertext: str, min_len: int = 3) -> dict[str, list[int]]:
    texto = norm(ciphertext)
    res = {}
    largo = min_len
    while largo < len(texto):
        vistos = {}
        for i in range(len(texto) - largo + 1):
            trozo = texto[i:i + largo]
            if trozo in vistos:
                vistos[trozo].append(i)
            else:
                vistos[trozo] = [i]
        hay = False
        for t in vistos:
            if len(vistos[t]) > 1:
                res[t] = vistos[t]
                hay = True
        if not hay:
            break
        largo = largo + 1
    return res


def distances(ciphertext: str, min_len: int = 3) -> list[int]:
    rep = repeats(ciphertext, min_len)
    dist = []
    for t in rep:
        pos = rep[t]
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                d = pos[j] - pos[i]
                if d not in dist:
                    dist.append(d)
    dist.sort()
    return dist


def factor_tally(ciphertext: str, max_factor: int = 20) -> dict[int, int]:
    dist = distances(ciphertext)
    cuenta = {}
    for f in range(2, max_factor + 1):
        cuenta[f] = 0
        for d in dist:
            if d % f == 0:
                cuenta[f] = cuenta[f] + 1
    return cuenta

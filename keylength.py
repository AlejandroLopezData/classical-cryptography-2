# keylength.py
from measure import index_of_coincidence
from railfence import norm


def coset_ic(ciphertext: str, m: int) -> float:
    texto = norm(ciphertext)
    total = 0
    for i in range(m):
        total = total + index_of_coincidence(texto[i::m])
    return total / m


def find_key_length(ciphertext: str, max_m: int = 16, language: str = "en") -> int:
    val = []
    for m in range(1, max_m + 1):
        val.append(coset_ic(ciphertext, m))

    umbral = 0.9 * max(val) 
    for m in range(1, max_m + 1):
        if val[m - 1] >= umbral:
            return m
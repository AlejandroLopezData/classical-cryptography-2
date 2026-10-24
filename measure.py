from freq import LETTER_FREQUENCIES

#B1 — Index of coincidence (0.75) -----------------------------------------
def index_of_coincidence(text: str) -> float:
    texto = text.upper()
    cuentas = {}
    n = 0
    for letra in texto:
        if letra >= "A" and letra <= "Z":
            if letra in cuentas:
                cuentas[letra] = cuentas[letra] + 1
            else:
                cuentas[letra] = 1
            n = n + 1
    if n < 2:
        return 0.0
    suma = 0
    for letra in cuentas:
        suma = suma + cuentas[letra] * (cuentas[letra] - 1)
    return suma / (n * (n - 1))


#B2 — Cipher family classifier (1.0)- -----------------------------------------


umbral = 2.16

# chi-squared test of the practice 1
def chi_squared(text: str, table: dict[str, float]) -> float:
    counts = {}
    for let in text.lower():
        if let in table:
            counts[let] = counts.get(let, 0) + 1
    n = sum(counts.values())
    chisq = 0.0
    for let in table:
        obs = counts.get(let, 0)
        exp = table[let] * n
        val = (obs - exp) ** 2 / exp
        chisq += val
    return chisq / n


def classify(ciphertext: str, language: str = "en") -> str:
    if chi_squared(ciphertext, LETTER_FREQUENCIES[language]) < umbral:
        return "transposition"
    return "substitution"
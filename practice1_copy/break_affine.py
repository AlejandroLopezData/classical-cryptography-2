from practice1_copy.frequencies import LETTER_FREQUENCIES
from practice1_copy.basics import alphabet
from practice1_copy.caesar import decrypt_cesar
from practice1_copy.affine import decrypt_affine, valid_keys_affine
from practice1_copy.vigenere import cosets, decrypt_vigenere
from practice1_copy.break_caesar import chi_squared

#C2 — Affine breaker ---------------------------------------------------------

# we use the same logic as in the cesars but now we try not the 26 option, we try the +200 comb of a and b.
# but in the core the brute force mechanism is the same as the cesars.
def break_affine(ciphertext: str, language: str = "en") -> tuple[tuple[int, int], str]:
    table = LETTER_FREQUENCIES[language]

    bk = (0, 0)
    bst_chi = float("inf")
    bst_txt = ""

    for a, b in valid_keys_affine():
        txt = decrypt_affine(ciphertext, a, b)
        chiv = chi_squared(txt, table)

        if chiv < bst_chi:
            bk = (a, b)
            bst_chi = chiv
            bst_txt = txt

    return bk, bst_txt
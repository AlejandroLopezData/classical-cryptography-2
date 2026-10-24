from practice1_copy.frequencies import LETTER_FREQUENCIES
from practice1_copy.basics import alphabet
from practice1_copy.caesar import decrypt_cesar
from practice1_copy.affine import decrypt_affine, valid_keys_affine
from practice1_copy.vigenere import cosets, decrypt_vigenere
from practice1_copy.break_caesar import chi_squared,break_caesar


# C3 — Vigenère breaker, key length given ---------------------------------------------------------

# given the length we can solve it trying combinations of cosets with the cesars method
def break_vigenere(ciphertext: str, m: int, language: str = "en") -> tuple[str, str]:
    key = ""
    coset_list= cosets(ciphertext, m)

    for coset in coset_list:
        k, txt = break_caesar(coset, language)
        key += alphabet[k % 26]

    text = decrypt_vigenere(ciphertext, key)

    return key, text

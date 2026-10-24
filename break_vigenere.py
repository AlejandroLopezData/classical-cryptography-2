from railfence import norm
from keylength import find_key_length
from practice1_copy.vigenere import cosets, decrypt_vigenere 
from practice1_copy.break_caesar import break_caesar                   

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def attack(ciphertext: str, language: str = "en") -> tuple[str, str]:
    texto = norm(ciphertext)
    m = find_key_length(texto, 16, language)
    clave = ""
    for c in cosets(texto, m):
        k, nada = break_caesar(c, language)
        clave = clave + abc[k]
    return clave, decrypt_vigenere(texto, clave)
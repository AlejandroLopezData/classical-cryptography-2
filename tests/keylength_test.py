
from railfence import norm
from practice1_copy.vigenere import encrypt_vigenere    
from keylength import coset_ic, find_key_length

texto = norm(open("data/text.txt").read())
clave = "SECRET"
k = len(clave)
cifrado = encrypt_vigenere(texto, clave)

print("| m | coset_ic | mark |")
print("|---|----------|------|")
for m in range(1, 17):
    if m == k:
        nota = "TRUE key length"
    elif m % k == 0:
        nota = "multiple"
    elif k % m == 0:
        nota = "divisor"
    else:
        nota = ""
    print("| %d | %.4f | %s |" % (m, coset_ic(cifrado, m), nota))

print("find_key_length ->", find_key_length(cifrado), "(true: %d)" % k)

#   Execute
#   python -m tests.keylength_test
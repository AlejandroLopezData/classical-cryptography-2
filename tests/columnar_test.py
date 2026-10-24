from columnar import key_order, encrypt, decrypt, encrypt_double, decrypt_double
from railfence import norm

def test_columnar():
    print("-----------------------------------")
    print("Tests for columnar.py")
    print("-----------------------------------")
    print("enigma:",key_order("ENIGMA"))
    print("rotor:",key_order("ROTOR"))
    print("kasiski:",key_order("KASISKI"))
    print("bletchley:",key_order("BLETCHLEY"))
    print("cipher:",encrypt("MYSECRETMESSAGE", "CIPHER"))
    print("kasiski:",encrypt("THE INDEX OF COINCIDENCE", "KASISKI"))
    print("doble enryption(rotor + enigma):",encrypt_double("THESAMEKEYMUSTNEVERBEUSEDTWICE", "ROTOR", "ENIGMA"))
    print("-----------------------------------")

test_columnar()

#   Execute
#   python -m pytest tests/columnar_test.py
#   python -m tests.columnar_test
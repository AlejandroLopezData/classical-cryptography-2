from railfence import encrypt, decrypt, norm

def test_rail():
    print("-----------------------------------")
    print("tests for railfence.py")
    print("-----------------------------------")
    print("encrypt(MYSECRETMESSAGE, 2) ==",encrypt("MYSECRETMESSAGE", 2))
    print("encrypt(MYSECRETMESSAGE, 3) ==",encrypt("MYSECRETMESSAGE", 3))
    print("encrypt(MYSECRETMESSAGE, 4) ==",encrypt("MYSECRETMESSAGE", 4))
    print("-----------------------------------")

test_rail()

#   Execute
#   python -m pytest tests/railfence_test.py
#   python -m tests.railfence_test

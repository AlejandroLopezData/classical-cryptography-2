from kasiski import repeats, distances, factor_tally

def test_kasiski():
    cifrado = ("ELQYR JVQDR LXEGB ELQQV ALQFE PTQOG DEZRG SIDSC PEFGO PXDOL "
               "ELQYR JXAOA LPKGV D")
    rep = repeats(cifrado)
    print(rep["ELQ"])
    mas_largo = ""
    for t in rep:
        if len(t) > len(mas_largo):
            mas_largo = t
    print(mas_largo, rep[mas_largo])
    print(distances(cifrado))
    print(factor_tally(cifrado))

test_kasiski()
#   Execute
#   python -m pytest tests/kasiski_test.py
#   python -m tests.kasiski_test
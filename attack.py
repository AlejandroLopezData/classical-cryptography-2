import argparse
import sys
from railfence import norm
from freq import LETTER_FREQUENCIES
import measure
from measure import index_of_coincidence, chi_squared, classify
from keylength import coset_ic, find_key_length
from break_vigenere import attack as attack_vigenere
from break_columnar import attack as attack_columnar, puntuar


def main():
    p = argparse.ArgumentParser(prog="attack.py")
    p.add_argument("--in", dest="input_file")
    p.add_argument("--lang", choices=["en", "es"], default="en")
    p.add_argument("--cols", type=int)
    args = p.parse_args()
    lang = args.lang

    # leer el cifrado
    if args.input_file is None:
        texto = norm(sys.stdin.read())
    else:
        texto = norm(open(args.input_file, encoding="utf-8").read())
    n = len(texto)

    # medidas
    tabla = LETTER_FREQUENCIES[lang]
    ic = index_of_coincidence(texto)
    chi = chi_squared(texto, tabla)
    familia = classify(texto)
    ic_idioma = sum(f * f for f in tabla.values()) / sum(tabla.values()) ** 2
    ic_umbral = (1 / 26 + ic_idioma) / 2
    print("--------------------------------------------------------------------------")
    print(" *** Automated attack of (substitution or transposition) ciphers ***")
    print("--------------------------------------------------------------------------")
    print("-- Measures -------------------------------------------------------------")
    print("language:", lang)
    print("letters:", n)
    print("index of coincidence: %.4f (%s: %.4f, random: %.4f)"
          % (ic, lang, ic_idioma, 1 / 26))
    print("chi-squared: %.4f | threshold: %s" % (chi, measure.umbral))
    print("family (chi-squared vs threshold):", familia)
    print("IC threshold between mono and poly: %.4f" % ic_umbral)
    print("--------------------------------------------------------------------------")

    # transposicion
    if familia == "transposition":
        print("*- Decision: transposition")
        print("--------------------------------------------------------------------------")
        if args.cols:
            if n % args.cols != 0:
                print("error: %d does not divide the length %d" % (args.cols, n))
                sys.exit(1)
            candidatos = [args.cols]
            print("columns given by --cols:", args.cols)
        else:
            candidatos = [c for c in range(2, 9) if n % c == 0]
            print("divisors of %d from 2 to 8: %s" % (n, candidatos))
            if len(candidatos) == 0:
                print("no divisor between 2 and 8, use --cols")
                sys.exit(1)
        print("--------------------------------------------------------------------------")
        mejor = None
        for c in candidatos:
            orden, claro = attack_columnar(texto, c, lang)
            punt = puntuar(claro)
            print("cols = %d | score = %.2f" % (c, punt))
            if mejor is None or punt > mejor[0]:
                mejor = (punt, c, orden, claro)
        print("--------------------------------------------------------------------------")
        print("best: %d columns" % mejor[1])
        print("column order:", mejor[2])
        print("--plaintext:-----------------------------------------------------------------------")
        print(mejor[3])
        print("--------------------------------------------------------------------------")


    # monoalfabetico
    elif ic >= ic_umbral:
        print("*- Decision: monoalphabetic substitution")
        print("--------------------------------------------------------------------------")
        print("not solved automatically, use frequency analysis")
        print("--------------------------------------------------------------------------")


    # polialfabetico
    else:
        print("*- Decision: polyalphabetic substitution")
        print("--------------------------------------------------------------------------")
        valores = [coset_ic(texto, m) for m in range(1, 17)]
        umbral = 0.9 * max(valores)
        print("coset_ic for m = 1..16 (threshold = 0.9 * max = %.4f):" % umbral)
        print("--------------------------------------------------------------------------")
        for m in range(1, 17):
            marca = ""
            if valores[m - 1] >= umbral:
                marca = "<- above threshold"
            print("%2d | %.4f | %s" % (m, valores[m - 1], marca))
        print("--------------------------------------------------------------------------")
        print("key length:", find_key_length(texto, 16, lang))
        solvedkey, solution = attack_vigenere(texto, lang)
        print("key:", solvedkey)
        print("--plaintext:------------------------------------------------------------------------")
        print(solution)

main()

#python attack.py --in data/cipher_vig.txt
#python attack.py --in data/cipher_col.txt
#python attack.py --in data/cipher_mono.txt
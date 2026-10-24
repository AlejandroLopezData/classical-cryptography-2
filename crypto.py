import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "practice1_copy"))

from practice1_copy.caesar import encrypt_cesar, decrypt_cesar
from practice1_copy.affine import encrypt_affine, decrypt_affine
from practice1_copy.monoalpha import encrypt_mono, decrypt_mono, key_from_keyword_affine
from practice1_copy.vigenere import encrypt_vigenere, decrypt_vigenere
from practice1_copy.break_caesar import break_caesar
from practice1_copy.break_affine import break_affine
from practice1_copy.break_vigenere import break_vigenere
from railfence import norm, encrypt as encrypt_railfence, decrypt as decrypt_railfence
from columnar import encrypt as encrypt_columnar, decrypt as decrypt_columnar
from measure import index_of_coincidence, chi_squared, classify
from kasiski import distances, factor_tally
from freq import LETTER_FREQUENCIES


def build_parser():
    parser = argparse.ArgumentParser(prog="crypto.py", description="Cryptography command-line tool")
    ciphers = parser.add_subparsers(dest="cipher", required=True)

    def io(p, lang=False):
        p.add_argument("--in", dest="input_file")
        p.add_argument("--out", dest="output_file")
        if lang:
            p.add_argument("--lang", choices=["en", "es"])

    # caesar
    caesar = ciphers.add_parser("caesar")
    modes = caesar.add_subparsers(dest="mode", required=True)
    for mode in ("encrypt", "decrypt"):
        p = modes.add_parser(mode)
        p.add_argument("--key", type=int, required=True)
        io(p, True)

    # affine
    affine = ciphers.add_parser("affine")
    modes = affine.add_subparsers(dest="mode", required=True)
    for mode in ("encrypt", "decrypt"):
        p = modes.add_parser(mode)
        p.add_argument("--a", type=int, required=True)
        p.add_argument("--b", type=int, required=True)
        io(p, True)

    # monoalphabetic
    mono = ciphers.add_parser("mono")
    modes = mono.add_subparsers(dest="mode", required=True)
    for mode in ("encrypt", "decrypt"):
        p = modes.add_parser(mode)
        p.add_argument("--keyword", required=True)
        io(p, True)

    # vigenere
    vigenere = ciphers.add_parser("vigenere")
    modes = vigenere.add_subparsers(dest="mode", required=True)
    for mode in ("encrypt", "decrypt"):
        p = modes.add_parser(mode)
        p.add_argument("--key", required=True)
        io(p, True)

    # railfence (nuevo)
    rail = ciphers.add_parser("railfence")
    modes = rail.add_subparsers(dest="mode", required=True)
    p = modes.add_parser("encrypt")
    p.add_argument("--rails", type=int, required=True)
    io(p)

    # columnar (nuevo)
    col = ciphers.add_parser("columnar")
    modes = col.add_subparsers(dest="mode", required=True)
    for mode in ("encrypt", "decrypt"):
        p = modes.add_parser(mode)
        p.add_argument("--key", required=True)
        io(p)

    # measure (nuevo)
    me = ciphers.add_parser("measure")
    kinds = me.add_subparsers(dest="measure_type", required=True)
    for name in ("ic", "classify", "kasiski"):
        p = kinds.add_parser(name)
        p.add_argument("--in", dest="input_file", required=True)
        p.add_argument("--lang", choices=["en", "es"], default="en")

    # break
    br = ciphers.add_parser("break")
    breaks = br.add_subparsers(dest="break_type", required=True)

    p = breaks.add_parser("caesar")
    p.add_argument("--in", dest="input_file", required=True)
    p.add_argument("--lang", choices=["en", "es"])

    p = breaks.add_parser("affine")
    p.add_argument("--in", dest="input_file", required=True)

    p = breaks.add_parser("vigenere")
    p.add_argument("--m", type=int, required=True)
    p.add_argument("--in", dest="input_file", required=True)

    return parser


def read_input(filename):
    if filename is None:
        return sys.stdin.read()
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_output(text, filename):
    if filename is None:
        print(text, end="")
        return
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        text = read_input(getattr(args, "input_file", None))

        if args.cipher == "caesar":
            if args.mode == "encrypt":
                result = encrypt_cesar(text, args.key)
            else:
                result = decrypt_cesar(text, args.key)

        elif args.cipher == "affine":
            if args.mode == "encrypt":
                result = encrypt_affine(text, args.a, args.b)
            else:
                result = decrypt_affine(text, args.a, args.b)

        elif args.cipher == "mono":
            key = key_from_keyword_affine(args.keyword)
            if args.mode == "encrypt":
                result = encrypt_mono(text, key)
            else:
                result = decrypt_mono(text, key)

        elif args.cipher == "vigenere":
            if args.mode == "encrypt":
                result = encrypt_vigenere(text, args.key)
            else:
                result = decrypt_vigenere(text, args.key)

        elif args.cipher == "railfence":
            result = encrypt_railfence(text, args.rails)

        elif args.cipher == "columnar":
            if args.mode == "encrypt":
                result = encrypt_columnar(text, args.key)
            else:
                result = decrypt_columnar(text, args.key)

        elif args.cipher == "measure":
            texto = norm(text)
            if args.measure_type == "ic":
                result = "IC = %.4f\n" % index_of_coincidence(texto)

            elif args.measure_type == "classify":
                chi = chi_squared(texto, LETTER_FREQUENCIES[args.lang])
                result = ("letters: %d\n"
                          "chi-squared: %.4f\n"
                          "IC: %.4f\n"
                          "class: %s\n" % (len(texto), chi,
                                           index_of_coincidence(texto),
                                           classify(texto)))

            else:  # kasiski
                top = sorted(factor_tally(texto).items(), key=lambda x: -x[1])[:5]
                result = "distances: %s\nfactor tally (top 5): %s\n" % (distances(texto), top)

        elif args.cipher == "break":
            if args.break_type == "caesar":
                result = break_caesar(text, args.lang)
            elif args.break_type == "affine":
                result = break_affine(text)
            else:
                result = break_vigenere(text, args.m)

        write_output(str(result), getattr(args, "output_file", None))

    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
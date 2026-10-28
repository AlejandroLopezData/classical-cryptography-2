# Cryptography II

*Transposition ciphers, statistical measurements, and automated attacks on classical ciphers in Python.*

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [How to Run Everything](#2-how-to-run-everything)
3. [Q&A](#3-qa)
4. [Question](#4-question)
5. [Anything that does not work, stated plainly](#5-anything-that-does-not-work-stated-plainly)
6. [LLM Usage](#6-llm-usage)

---

## 1. Introduction

This project is a command-line toolkit for classical cryptography, written in pure Python. It extends the Practice 1 tool (Caesar, affine, monoalphabetic and Vigenère ciphers with their attacks) with two transposition ciphers, rail fence and columnar, and with the statistical tools needed to analyze unknown ciphertexts.

---

## 2. How to Run Everything

### 2.1 Automated Attack

```bash
python attack.py --in cipher.txt [--lang en|es] [--cols N]
```

- `--lang` *Optional*, default is `en`
- `--cols` *Optional*, gives the number of columns for a transposition break. Without it, every divisor of the ciphertext length from 2 to 8 is tried and the best bigram score wins.

`attack.py` takes a ciphertext, decides by itself which family it belongs to, and applies the matching attack. It prints the measurements behind each decision.

**1. Transposition**

*Columnar transposition:* the key length (number of columns) is given with `-cols` or found by trying the divisors of the ciphertext length from 2 to 8. The attack tries every column order and keeps the one that looks most like English.

**2. Substitution**

*Monoalphabetic:* detected and reported. It is not solved automatically.

*Polyalphabetic (Vigenère):* the key length is estimated, each coset is broken as a Caesar cipher, and the tool prints the key and the plaintext.

You can test them with pre cyphered texts:

```bash
# Transposition cypher test
python attack.py --in data/cipher_col.txt

# Monoalphabetic test
python attack.py --in data/cipher_mono.txt

# Polyalphabetic Vigenere test
python attack.py --in data/cipher_vig.txt
```

### 2.2 Commands

The program is executed from the command line using:

```bash
python3 crypto.py <command> <action> [options]
```

#### 2.2.1 Practice 1 Ciphers

| Cipher | Action | Command |
| --- | --- | --- |
| **Caesar** | Encrypt | `python3 crypto.py caesar encrypt --key 3 --in message.txt --out cipher.txt` |
| | Decrypt | `python3 crypto.py caesar decrypt --key 3 --in cipher.txt --out message.txt` |
| | Break | `python3 crypto.py break caesar --in cipher.txt --lang en` |
| **Affine** | Encrypt | `python3 crypto.py affine encrypt --a 5 --b 8 --in message.txt --out cipher.txt` |
| | Decrypt | `python3 crypto.py affine decrypt --a 5 --b 8 --in cipher.txt --out message.txt` |
| | Break | `python3 crypto.py break affine --in cipher.txt` |
| **Monoalphabetic** | Encrypt | `python3 crypto.py mono encrypt --keyword CRYPTO --in message.txt --out cipher.txt` |
| | Decrypt | `python3 crypto.py mono decrypt --keyword CRYPTO --in cipher.txt --out message.txt` |
| **Vigenère** | Encrypt | `python3 crypto.py vigenere encrypt --key LEMON --in message.txt --out cipher.txt` |
| | Decrypt | `python3 crypto.py vigenere decrypt --key LEMON --in cipher.txt --out message.txt` |
| | Break | `python3 crypto.py break vigenere --m 5 --in cipher.txt` |

> **Notes:** `--lang` sets the language for frequency analysis. The value of `a` must be coprime with 26. The keyword builds the substitution alphabet. `--m` is the assumed Vigenère key length.

#### 2.2.2 Rail Fence Cipher

**Encrypt**

```bash
python3 crypto.py railfence encrypt --rails 3 --in message.txt --out cipher.txt
```

#### 2.2.3 Columnar Transposition Cipher

**Encrypt**

```bash
python3 crypto.py columnar encrypt --key CIPHER --in message.txt --out cipher.txt
```

**Decrypt**

```bash
python3 crypto.py columnar decrypt --key CIPHER --in cipher.txt --out message.txt
```

> The text is written in rows under the key and read by columns in the alphabetical order of the key letters. An incomplete last row is padded with `X`, so the decrypted text can end with extra X.

**Breaking (using the automated attack)**

```bash
python3 attack.py --in cipher.txt --cols 6
python3 attack.py --in cipher.txt
```

- `--cols` gives the number of columns. Without it, every divisor of the ciphertext length from 2 to 8 is tried and the best bigram score wins.

#### 2.2.4 Measurements

```bash
python3 crypto.py measure ic --in cipher.txt
python3 crypto.py measure classify --in cipher.txt
python3 crypto.py measure kasiski --in cipher.txt
```

- `ic` prints the index of coincidence.
- `classify` prints the number of letters, chi-squared, IC and the family (`transposition` or `substitution`).
- `kasiski` prints the repeated-sequence distances and the factor tally.

#### 2.2.5 Input and Output Files

The `--in` option specifies the input file. The `--out` option is optional. If it is provided, the result is written to that file. If not, the result is printed to the terminal:

```bash
python3 crypto.py columnar decrypt --key CIPHER --in cipher.txt
```

> Characters that are not part of the alphabet are ignored during encryption and decryption. Spaces and punctuation are not preserved in their original positions.

### 2.3 Test execution

You can run the following commands to execute the different tests and review their results:

```bash
# Tests the columnar transposition cipher-breaking algorithm
python -m tests.break_columnar_test

# Tests the Vigenère cipher-breaking algorithm
python -m tests.break_vigenere_test

# Tests the columnar transposition cipher implementation
python -m tests.columnar_test

# Tests the Kasiski examination method for analysing Vigenère ciphers
python -m tests.kasiski_test

# Tests the key length estimation algorithm
python -m tests.keylength_test

# Tests the cipher classification based on statistical measurements
python -m tests.measure_class_test

# Tests the Index of Coincidence (IC) calculation
python -m tests.measure_IC_test

# Tests the Rail Fence cipher implementation
python -m tests.railfence_test
```

---

## 3. Q&A

### 3.1 A3 — Double Transposition Padding

> That plaintext is 30 letters, and 30 is a multiple of both key lengths, so no padding is needed at either pass. Explain what your decrypt_double has to do differently when the plaintext length is not a multiple of both, and why a naive implementation returns garbage in that case.

Given n the text length, k1/k2 the key lengths, L1 = "n rounded up to the next multiple of k1" (first pass) and L2 = "L1 rounded up to the next multiple of k2" (second pass).

If n is a multiple of k1 and k2, then L1 = L2 = n, no problem. But if L2 > L1, the second pass adds L2 - L1 padding letters to the end of the first output. If we undo kw2, L2 letters are obtained, but only the first L1 are the real output.

What decrypt_double has to do differently: after undoing kw2, it must remove the last L2 - L1 letters before undoing kw1, so that the second decrypt receives exactly L1 letters (a multiple of k1). In my implementation this is done by cutting the text to the largest multiple of k1 that fits in L2. It does not know n, so this is exact when k1 >= k2, because there is only one possible multiple of k1 in that range. The result still includes the padding of the first pass, as decrypt returns the padded plaintext.

A naive implementation applies decrypt with kw1 directly to the L2 letters. Decrypt measures the height of the columns as rows = L2 // k1, but the first pass used rows = L1 // k1. With a wrong height the ciphertext is divided into segments of the wrong size. Each segment is placed in a wrong column, all the letters shift and the result is incorrect.

**Example**

```
n = 10, k1 = 3, k2 = 5, L1 = 12, L2 = 15
```

The naive implementation would use columns of 5 instead of 4.

With the test example (30 letters and keys of 5 and 6) it works because L1 = L2 = 30 and there is no padding.

---

### 3.2 B1 — Minimum Text Length for IC

> CRYPTANALYSIS is an English word whose index equals that of uniformly random letters. State the shortest text length at which you would trust this measurement, and how you decided.

CRYPTANALYSIS has 13 letters, so there are only 13*12/2 = 78 pairs of positions. Its IC is 0.0385, which equals the value for uniformly random letters (expected IC about 0.0667).

To decide the minimum length I have created 3 different texts and measured their IC. The results are that even with 50 letters you can stay over the random distance.

The three generated texts are above the typical english IC (0.0667).

You cannot say that every text of 50 letters will be over the randomness so I would say that there is an interval in which a text could be over the english IC and I would say that is around the 50 to 60 letters.

| Text | n letters | IC | random distance (0.0385) |
| --- | ---: | ---: | ---: |
| CRYPTANALYSIS | 13 | 0.0385 | 0 |
| txt50 | 50 | 0.0947 | 0.056 |
| txt80 | 80 | 0.0823 | 0.044 |
| txt100 | 100 | 0.0745 | 0.036 |

---

### 3.3 B2 — Classifier Threshold

The threshold (2.16) was selected by testing different values and choosing the one with the fewest errors. It is defined in `measure.py` and verified by `tests/measure_class_test.py`.

#### 3.3.1 Measurement Task

```
      |             pad X           |            pad azar
 leng | transp. error | sust. error | transp. error | sust. error
   60 |         18.7% |        0.7% |          0.0% |        0.0%
  120 |          1.3% |        1.3% |          0.0% |        0.0%
  250 |          0.0% |        1.3% |          0.0% |        0.0%
  400 |          0.0% |        1.3% |          0.0% |        0.0%
```

#### 3.3.2 At which lengths does the classifier work, and at which does it fail?

As we can see on the table, with pad X it works from 120 letters upward and fails at 60, where 18.7% of transpositions are misclassified as substitution. With a random pad it works at every length tested with no error for both transposition and substitution ciphers.

#### 3.3.3 Changing only the pad character moves the error rate substantially. Explain the mechanism.

Transposition keeps the english letter frequencies, so its chi squared is low. A constant pad X is a rare letter in English, so each extra X adds a huge amount to chi squared.

The pad matters most in short texts. Changing only the pad drops the error at 60 letters from 18.7% to 0.0%, because random letters from the English distribution add almost nothing to the chi squared value.

#### 3.3.4 Compute, for a 66-letter ciphertext containing 6 pad characters, how much the pad alone contributes to the chi-squared statistic. Compare that number with your threshold.

In my frequency table, X has a frequency of 0.0015. In a 66-letter text we expect only 66 x 0.0015 = 0.099 X, but the ciphertext has 6. The pad’s contribution to chi squared is (6 − 0.099)² / 0.099 = 351.7, normalized by length = 351.7 / 66 = **5.33**.

I checked this with my own function. 60 letters of English give a chi squared of 0.257, and adding 6 (X) gives 5.548. The pad adds about **5.29.** My threshold is 2.16 so the text is classified as a substitution though it’s in reality a transposition.

#### 3.3.5 State the design rule this implies for anyone building a cipher that needs padding

Though constant padding breaks our classifier, it must be statistically indistinguishable from the plaintext because it can reveal that a padding exists, how much there is, and leave a fixed fingerprint in every message.

---

### 3.4 B3 — `factor_tally` vs gcd

> The greatest common divisor of those three distances is 5, which is the right answer. Explain why your factor_tally must not be replaced by a gcd, and give the condition under which the gcd silently fails.

**Why `factor_tally` must not be replaced by a gcd**

The gcd needs **all** the distances to be multiples of the key length. `factor_tally` is different: it **counts votes**. For each factor, it counts how many distances are divisible by it, and the factor with the most votes is the best guess for the key length.

This matters because Kasiski's method can find **accidental repeats**, which are repeated strings that appear by pure chance. Their distances have nothing to do with the key length.

**When the gcd silently fails**

The gcd fails when **at least one distance is accidental**, meaning it is not a multiple of the real key length *k*. In that case the gcd drops to 1 (or to some wrong small number). It does not give an error, so the failure is *silent*: you just get a valid-looking but wrong answer.

**Example**

Suppose the real key length is 5. Our distances are 15, 35 and 50, and a random repeat adds a fourth distance, 17:

```
distances = [15, 35, 50, 17]
gcd       = 1        <- wrong, we lost the key length
factor_tally[5] = 3  <- still the winner (3 votes out of 4)
```

One bad distance is enough to ruin the gcd, but `factor_tally` still points to 5.

**In our actual output**

With 15, 35 and 50 there is no accidental distance, so the gcd is 5 and it matches `factor_tally` (`5: 3`). But that is only luck: the gcd works here only because the data is clean.

> **Conclusion:** the gcd is fragile because it needs all distances to be correct, while `factor_tally` is robust because it only needs most of them.

---

### 3.5 C1 — `coset_ic` Table

> Show the full table of coset_ic for m = 1 to 16 on one of your own test ciphertexts, and mark the true key length, its multiples and its divisors.

`coset_ic(ciphertext, m)` splits the ciphertext into m cosets and returns the average of their indices of coincidence. `find_key_length` computes it for m = 1 to 16 and returns the smallest m that is clearly above the baseline.

Taking the largest average would return a multiple of the key length, so I return the smallest m above the threshold.

I chose 0.9 threshold because the multiples of the key length are aligned, so their cosets have a similar Caesar shift and a higher IC. Other values mix different shifts and have a lower IC. The highest non aligned value is 0.0610 (m = 15), while the lowest aligned value is 0.0757 (m = 6). With 0.9, the threshold is 0.0693, which is between these values.

| m | coset_ic | mark |
| ---: | ---: | --- |
| 1 | 0.0490 | divisor |
| 2 | 0.0527 | divisor |
| 3 | 0.0601 | divisor |
| 4 | 0.0536 | |
| 5 | 0.0489 | |
| **6** | **0.0757** | **TRUE key length** |
| 7 | 0.0493 | |
| 8 | 0.0535 | |
| 9 | 0.0594 | |
| 10 | 0.0522 | |
| 11 | 0.0477 | |
| **12** | **0.0770** | **multiple** |
| 13 | 0.0494 | |
| 14 | 0.0521 | |
| 15 | 0.0610 | |
| 16 | 0.0527 | |

---

### 3.6 C2 — Automatic Vigenère Attack

`attack` finds the key length with `find_key_length`, splits the ciphertext into cosets, breaks each coset with `break_caesar` and joins the letters into the key. 100 trials per cell, random keys and random windows of my reference text.

#### 3.6.1 The two tables degrade at very different rates. Which quantity governs each?

Table 1 (complete key) is governed by the number of letters per coset. Each coset is a Caesar cipher, and the breaker needs enough letters for the frequencies to be reliable. All cosets must be correct at once, because an error in any coset results in an incorrect key. Therefore, the full key degrades fast.

Table 2 (key length) degrades much more slowly. It only needs the aligned values of `coset_ic` to stand out from the others, which depends on the total n and on the selection rule.

#### 3.6.2 Your attack succeeds on a 200-letter ciphertext with a 5-letter key and fails on a 200-letter ciphertext with a 9-letter key. Explain why, in terms of the quantity you identified.

With a key length of 5, each coset has about 200/5 = 40 letters, and the key is recovered 99% of the time. With a length of 9, each coset has about 200/9 = 22.22 letters, the key is recovered 88% of the time. The attack fails with the longer key because each coset contains fewer letters, making the break_caesar fail.

---

### 3.7 C3 — Columnar Transposition Breaker

| cols \ n | 60 | 120 | 200 |
| ---: | ---: | ---: | ---: |
| 4 | 100% | 100% | 100% |
| 5 | 99% | 100% | 100% |
| 6 | 97% | 100% | 100% |
| 7 | 98% | 100% | 100% |

The largest number of columns (n) that can be handled in a 10 second window is eight. n = 9 takes 11.67 sec and n = 8 1.26 sec.

The applied complexity of the breaker is O(n!), and its complexity can be improved with a different approach. We start with a random column order and score it with the bigram log probability. Then try swapping two columns. If the score improves, keep the swap. If not improves, undo it. Repeat until no swap improves the score, and run it from a few random starts, keeping the best result.

With this approach we turn the complexity to O( n^2 / 2), the work grows slowly and handles a much larger n. The trade off is that you don’t guarantee the best ordering because it can get stuck in a local maximum.

---

## 4. Question

> One paragraph: your Part D pipeline makes a decision from a single number before it tries any attack. Name the one cipher property that number depends on, and describe a cipher that would defeat the classifier entirely.

The classifier decides using one number: the “chi-squared” of the letter counts against the language. So it depends on one property: **whether the cipher keeps the letter frequencies of the plaintext**.

A transposition only moves letters, so the frequencies stay the same and the chi-squared is low. A substitution changes the letters, so the chi-squared is high.

A cipher that defeats it is a **substitution followed by a transposition**. The chi-squared is high, so the tool says “substitution” and never tries the columnar attack, but the letters are also shuffled in position, so the frequency assistant’s output is useless. The classifier gives a wrong answer without any warning, because it only looks at one number.

---

## 5. Anything that does not work, stated plainly

Though the automated attack implemented in `attack.py` is complete, the missing frequency analysis code from Practice 1 makes impossible to provide the full analysis. The attack successfully identifies the cipher as a monoalphabetic substitution cipher, but it only reports the measurements and the cipher family without providing the detailed analysis.

---

## 6. LLM Usage

Claude was used as a tool to help the development and testing process:

1. **Complex tests:** Assistance with programming some complex tests as the `tests/measure_test.py` one.
2. **Test data generation:** Generation of random text samples for testing purposes.
3. **Command line interface:** Assistance with implementing the CLI interface in `crypto.py`.
4. **Readme documentation:** To help transforming my Notion documentation and answers into markdown code for the README.MD and for the .gitignore creation

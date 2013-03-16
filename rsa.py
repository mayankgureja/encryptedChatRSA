"""
rsa.py
Mayank Gureja
03/14/2013
"""


import random
import fractions


def coPrime(x):
    """
    Finds a random co-prime of given number
    """

    n = x * 2 + 100000  # Upper limit for range of random integers
    y = random.randint(x * 2, n)
    if (fractions.gcd(x, y) != 1):
        return coPrime(x)
    else:
        return y


def mod_inverse(base, m):
    """
    Calculates modular multiplicate inverse
    """

    g, x, y = mod_inverse_iterative(base, m)
    if (g != 1):
        return None
    else:
        return (x % m)


def mod_inverse_iterative(a, b):
    """
    Helps mod_inverse work
    """

    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b / a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return b, x, y


def modulo(a, b, c):
    """
    Calculates modulo
    """
    return ((int(a) ** int(b)) % int(c))


def totient(n):
    """
    Calculates Euler's totient
    """

    count = 0
    for i in range(1, n):
        if (fractions.gcd(n, i) == 1):
            count = count + 1

    return count


def gen_prime():
    """
    Generates random prime numbers between 2 and n
    """

    n = 100
    if n == 2:
        return [2]
    elif n < 2:
        return []
    s = range(3, n + 1, 2)
    mroot = n ** 0.5
    half = (n + 1) / 2 - 1
    i = 0
    m = 3
    while m <= mroot:
        if s[i]:
            j = (m * m - 3) / 2
            s[j] = 0
            while j < half:
                s[j] = 0
                j += m
        i = i + 1
        m = 2 * i + 3
    primes = [2] + [x for x in s if x]
    return (primes[random.randint(1, len(primes) - 1)])


def prime_factors(n):
    """
    Factorizes given prime number
    """

    factors = []
    lastresult = n
    c = 2
    while lastresult != 1:
        if lastresult % c == 0 and c % 2 > 0:
            factors.append(c)
            lastresult /= c
            c += 1
        else:
            c += 1
    return factors[0], factors[1]


def endecrypt(x, e, c):
    """
    Encrpyts/decrypts given ASCII character value, via the RSA crypto algorithm
    """

    return modulo(x, e, c)


def decode(x):
    """
    Decodes given ASCII character value into ASCII character
    """

    try:
        return str(unichr(x).encode('ascii', 'replace'))  # Make sure data is encoded properly
    except ValueError as err:
        print err
        print "** ERROR - Decoded character is unrecognized **"


def key_cracker(e, c):
    """
    RSA Key Cracker
    """

    print "Public Key: (%0d, %0d)" % (e, c)
    a, b = prime_factors(c)
    print "[a, b] : [%0d, %0d]" % (a, b)
    m = (a - 1) * (b - 1)
    print "Totient: %0d" % (totient(m))
    d = mod_inverse(e, m)

    return d


def keygen():
    """
    Generates random RSA keys
    """

    a = gen_prime()
    b = gen_prime()
    if a == b:
        keygen()

    c = a * b
    m = (a - 1) * (b - 1)
    e = coPrime(m)
    d = mod_inverse(e, m)

    return (e, d, c)


def test_helpers():
    """
    Test function for utility functions
    """

    print "GCD of 8 and 12 is %0d" % fractions.gcd(8, 12)

    print "%0d and %0d are co-prime" % (2, coPrime(2))
    print "%0d and %0d are co-prime" % (6, coPrime(6))

    mod_inverse(11, 60)

    modulo(2, 3, 4)

    totient(24)


def test_encryption(e, c):
    """
    Test function for encryption
    """

#	e = int(raw_input("\nEnter e from public key\n"))
#	c = int(raw_input("\nEnter c from public key\n"))

    string = raw_input("\nEnter word to encrpyt\n")
    for i in range(0, len(string)):
        print endecrypt(ord(string[i]), e, c)


def test_decryption(d, c):
    """
    Test function for decryption
    """

#	d = int(raw_input("\nEnter d from public key\n"))
#	c = int(raw_input("\nEnter c from public key\n"))

    x = int(raw_input("\nEnter number to decrypt\n"))
    decode(endecrypt(x, d, c))


def test_endecrypt():
    """
    Runs all cryptographic method tests
    """

    e, d, c = keygen()

    test_encryption(e, c)
    test_decryption(d, c)
    key_cracker(e, c)


"""
Main
"""

# test_helpers()
# test_endecrypt()

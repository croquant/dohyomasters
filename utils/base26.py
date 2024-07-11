ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_LEN = len(ALPHABET)
BYTE_VALUES = 256
NOM = 851
DENOM = 500


def encode(src: bytes) -> str:
    src = bytearray(src)
    out = []
    out_length = (len(src) * NOM + DENOM - 1) // DENOM

    for _ in range(out_length):
        acc = 0
        for i in range(len(src) - 1, -1, -1):
            full_val = (acc * BYTE_VALUES) + int(src[i])
            full_val_mod = full_val % ALPHABET_LEN
            src[i] = (full_val - full_val_mod) // ALPHABET_LEN
            acc = full_val_mod
        out.append(ALPHABET[acc])

    return "".join(out)


def decode(s: str) -> bytes:
    s = bytearray(s, "ascii")
    out = bytearray()
    out_length = (len(s) * DENOM + NOM - 1) // NOM

    for _ in range(out_length):
        acc = 0
        for i in range(len(s) - 1, -1, -1):
            value = acc * ALPHABET_LEN + (s[i] - ord(ALPHABET[0]))
            s[i] = value // BYTE_VALUES + ord(ALPHABET[0])
            acc = value % BYTE_VALUES
        out.append(acc)

    if out and out[-1] == 0:
        out.pop()

    return bytes(out)

import csv
import json
import math
import sys

ERROR_CODE = -1

PRIME_NUMS_TABLE = (
    (2897, 5683),
    (2903, 5689),
    (2909, 5693),
    (2917, 5701),
    (2927, 5711),
    (2939, 5717),
    (2953, 5737),
    (2957, 5741),
    (2963, 5743),
    (2969, 5749),
    (2971, 5779),
    (2999, 5783)
)
ALPHABET = [''] + [chr(i) for i in range(ord('А'), ord('Я') + 1)]
BLOCK_LENGTH = 3


def is_prime(num: int):
    for i in range(2, math.ceil(math.sqrt(num))):
        if num % i == 0:
            return False
    return True


def find_nearest_prime(num: int):
    if is_prime(num):
        return num
    less = num - 1
    more = num + 1
    while True:
        if is_prime(less):
            return less
        elif is_prime(more):
            return more
        less -= 1
        more += 1


def mod_pow(num: int, exp: int, mod: int):
    _l = math.ceil(math.log(mod, 2))
    _w = 1
    _v = num
    _d = bin(exp).replace("0b", '')[::-1]
    for i in range(min(_l, len(_d))):
        if _d[i] == '1':
            _w = (_w * _v) % mod
        _v = (_v * _v) % mod
    return _w


def euclid_extended(_r1: int, _r2: int, _s1=1, _s2=0, _t1=0, _t2=1):
    if _r2 == 0:
        return [{"r1": _r1, "r2": _r2, "r": None, "g": None,
                 "s1": _s1, "s2": _s2, "s": None,
                 "t1": _t1, "t2": _t2, "t": None}]
    else:
        _g = int(_r1 / _r2)
        _r = _r1 % _r2
        _s = _s1 - _s2 * _g
        _t = _t1 - _t2 * _g
        return [{"r1": _r1, "r2": _r2, "r": _r1 % _r2, "g": _g,
                 "s1": _s1, "s2": _s2, "s": _s,
                 "t1": _t1, "t2": _t2, "t": _t}] \
               + euclid_extended(_r2, _r, _s2, _s, _t2, _t)


def encode_blocks(message: str):
    counter = BLOCK_LENGTH
    blocks_list = []
    block = 0
    for ch in message:
        counter -= 1
        block = block * 100 + ALPHABET.index(ch)
        if counter == 0:
            blocks_list.append(block)
            counter = BLOCK_LENGTH
            block = 0
    if block != 0:
        blocks_list.append(block)
    return blocks_list


def decode_blocks(blocks_list: list[int]):
    chars = []
    for block in blocks_list:
        for i in range(BLOCK_LENGTH)[::-1]:
            k = 100 ** i
            index = int(block / k)
            block = block % k
            if 0 <= index < len(ALPHABET):
                chars.append(ALPHABET[index])
            else:
                chars.append(str(index))
    return ''.join(chars)


def encrypt_blocks(blocks_list: list[int], key: int, mod: int):
    enc_blocks_list = []
    for block in blocks_list:
        enc_blocks_list.append(mod_pow(block, key, mod))
    return enc_blocks_list


def decrypt_blocks(blocks_list: list[int], key: int, mod: int):
    return encrypt_blocks(blocks_list, key, mod)


def save_values(
        p_save: int, g_save: int, n_save: int,
        es_save: int, e_save: int, fn_save: int,
        euclid_save: list, d_save: int, text_save: str,
        text_bl_save: list[int], encr_bl_save: list[int],
        decr_bl_save: list[int], msg_save: str,
):
    saving_data = []
    for i in range(len(ALPHABET)):
        saving_data.append((ALPHABET[i], i))

    saving_data.extend([(),
                        ("p =", p_save, "", "g =", g_save),
                        ("n =", n_save, "", "f(n) = (p-1)(g-1)", fn_save),
                        ("e\' =", es_save, "", "e =", e_save),
                        (),
                        ("i", "r1", "r2", "r", "g", "s1", "s2", "s", "t1", "t2", "t")])
    for i in range(len(euclid_save)):
        saving_data.append((i + 1, euclid_save[i]["r1"], euclid_save[i]["r2"], euclid_save[i]["r"],
                            euclid_save[i]["g"],
                            euclid_save[i]["s1"], euclid_save[i]["s2"], euclid_save[i]["s"],
                            euclid_save[i]["t1"], euclid_save[i]["t2"], euclid_save[i]["t"]))

    saving_data.extend([(),
                        ("НОД", "s", "a", "t", "b"),
                        (euclid_save[-1]["r1"], euclid_save[-1]["s1"],
                         euclid_save[0]["r1"], euclid_save[-1]["t1"],
                         euclid_save[0]["r2"]),
                        ("d = mod(t,f(n)) =", d_save),
                        (),
                        ("text", "block", "encrypt block", "decrypt block", "message")])

    for i in range(len(text_bl_save)):
        saving_data.append((text_save[i * BLOCK_LENGTH:i * BLOCK_LENGTH + 3],
                            text_bl_save[i], encr_bl_save[i], decr_bl_save[i],
                            msg_save[i * BLOCK_LENGTH:i * BLOCK_LENGTH + 3]))

    with open("output.csv", "w+", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerows(saving_data)


if __name__ == '__main__':
    n_s: int
    dd: int
    mm: int
    yyyy: int
    text: str
    try:
        with open("input.json", "r", encoding='utf-8') as json_file:
            reading_data = json.load(json_file)
            n_s = reading_data["N"]
            dd = reading_data["DD"]
            mm = reading_data["MM"]
            yyyy = reading_data["YYYY"]
            text = reading_data["FIRST_NAME"] \
                   + reading_data["SECOND_NAME"] \
                   + reading_data["FATHER_NAME"]
    except ValueError:
        sys.exit(ERROR_CODE)

    p = PRIME_NUMS_TABLE[n_s - 1][0]
    g = PRIME_NUMS_TABLE[n_s - 1][1]
    n = p * g
    es = 9000000 + mm * 10000 + dd * 100 + 13
    e = find_nearest_prime(es)
    fn = (p - 1) * (g - 1)
    all_euclid = euclid_extended(fn, e)
    d = all_euclid[-1]["t1"] % fn

    blocks = encode_blocks(text)
    encr_blocks = encrypt_blocks(blocks, e, n)
    encr_msg = decode_blocks(encr_blocks)
    decr_blocks = decrypt_blocks(encr_blocks, d, n)
    decr_msg = decode_blocks(decr_blocks)

    save_values(p, g, n, es, e, fn, all_euclid, d,
                text, blocks, encr_blocks, decr_blocks, decr_msg)
    print("SUCCESS")

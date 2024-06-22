from sha256 import _hash
import sys
import re


def normalize_spaces(input_string):
    spaced_string = ""
    for i, char in enumerate(input_string):
        spaced_string += char
        if (i + 1) % 8 == 0 and i != len(input_string) - 1:
            spaced_string += " "
    return spaced_string


def gc_to_bin(gc):
    return (
        [0, 0]
        if gc == "0"
        else [0, 1] if gc == "n" else [1, 0] if gc == "u" else [1, 1]
    )


def parse_log(order, msg_start, cv_start):
    msg_bitstr = ["", ""]
    cv_bitstr = ["", ""]
    seed, exit_code = 0, -1
    for line in sys.stdin:
        if line.startswith("v"):
            words = line.split()
            for word in words:
                if word == "v" or word == "0":
                    continue
                lit = int(word)
                value = "0" if lit < 0 else "1"
                lit_abs = abs(lit)
                if lit_abs >= msg_start[0] and lit_abs < msg_start[0] + 512:
                    msg_bitstr[0] += value
                elif lit_abs >= msg_start[1] and lit_abs < msg_start[1] + 512:
                    msg_bitstr[1] += value
                elif lit_abs >= cv_start[0] and lit_abs < cv_start[0] + 256:
                    cv_bitstr[0] += value
                elif lit_abs >= cv_start[1] and lit_abs < cv_start[1] + 256:
                    cv_bitstr[1] += value
        elif line.startswith("c"):
            match = re.search(r"--seed=(\d+)", line)
            if match:
                seed = int(match.group(1))
            elif line.startswith("c exit"):
                exit_code = int(line.split()[2])

    print(f"# {order} steps with seed {seed}\n")
    if exit_code == 10:
        assert len(msg_bitstr[0]) == 512
        assert len(msg_bitstr[1]) == 512
        assert len(cv_bitstr[0]) == 256
        assert len(cv_bitstr[1]) == 256

        cvs = [[], []]
        msgs = ["", ""]
        for k in range(2):
            for i in range(16):
                msg_word = msg_bitstr[k][i * 32 : (i + 1) * 32][::-1]
                word_int = int(msg_word, 2)
                msgs[k] += format(word_int, "08x")
            for i in range(8):
                cv_word = cv_bitstr[k][i * 32 : (i + 1) * 32][::-1]
                word_int = int(cv_word, 2)
                cvs[k].append(word_int)

        assert len(msgs[0]) == 512 / 4
        assert len(msgs[1]) == 512 / 4
        assert len(cvs[0]) == 8
        assert len(cvs[1]) == 8
        hashes = [_hash(order, msgs[0], cvs[0]), _hash(order, msgs[1], cvs[1])]

        h_0, h_0_prime = "", ""
        for value in cvs[0]:
            h_0 += "{:x}".format(value)
        for value in cvs[1]:
            h_0_prime += "{:x}".format(value)

        print(
            f"""| Variable | Value                                                                     |
|--------|---------------------------------------------------------------------------|
| $h_0$  | `{normalize_spaces(h_0)}` |
| $h'_0$ | `{normalize_spaces(h_0_prime)}` |
| $M$ | `{normalize_spaces(msgs[0])}` |
| $M'$ | `{normalize_spaces(msgs[1])}` |
| $h_1$ | `{normalize_spaces(hashes[0])}` |
| $h'_1$ | `{normalize_spaces(hashes[1])}` |
"""
        )

        # print("$h_0 = $  `" + normalize_spaces(h_0) + "`\n")
        # print("$h_0' = $ `" + normalize_spaces(h_0_prime) + "`\n")
        # print("$M = $ `" + normalize_spaces(msgs[0]) + "`\n")
        # print("$M' = $ `" + normalize_spaces(msgs[1]) + "`\n")
        # print("$h_1 = $  `" + normalize_spaces(hashes[0]) + "`\n")
        # print("$h_1' = $ `" + normalize_spaces(hashes[1]) + "`\n")
        assert hashes[0] == hashes[1]
        # print("Verified" if hashes[0] == hashes[1] else "Failed")
    else:
        print("Timed out\n")


def get_info(enc_path):
    order = 0
    msg_start = [0, 0]
    cv_start = [0, 0]
    with open(enc_path, "r") as enc:
        for line in enc.readlines():
            if line.startswith("c"):
                words = line.split()
                if len(words) != 3:
                    continue
                match words[1]:
                    case "cv_f":
                        cv_start[0] = int(words[2])
                    case "cv_g":
                        cv_start[1] = int(words[2])
                    case "W_0_f":
                        msg_start[0] = int(words[2])
                    case "W_0_g":
                        msg_start[1] = int(words[2])
                    case "order":
                        order = int(words[2])

    return {"msg_start": msg_start, "cv_start": cv_start, "order": order}


enc_path = sys.argv[1]
info = get_info(enc_path)
msg_start = info["msg_start"]
cv_start = info["cv_start"]
assert msg_start[0] != 0 and msg_start[1] != 0
assert cv_start[0] != 0 and cv_start[1] != 0
order = info["order"]
parse_log(order, msg_start, cv_start)

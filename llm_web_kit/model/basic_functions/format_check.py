
def is_en_letter(c: str):
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')


def is_space(c: str):
    return c in [' ', '\t']


def is_pure_en_word(s: str):
    for c in s:
        if is_en_letter(c) or is_space(c):
            continue
        return False
    return True

MAX_SIZE = 6000


def compress(text):

    if len(text) <= MAX_SIZE:
        return text

    return text[:MAX_SIZE]
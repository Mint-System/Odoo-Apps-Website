import unicodedata


def _unicode_to_ascii(string):
    # replace 'ß'
    string = string.lower().replace("ß", "ss")
    # Normalize to NFD (decomposes accented chars)
    normalized = unicodedata.normalize("NFD", string)
    # Keep only ASCII characters (i.e., discard combining diacritics)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    return ascii_only

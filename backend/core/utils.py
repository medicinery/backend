import nanoid as noid


def generate_id():
    return noid.generate(size=16, alphabet="0123456789abcdefghijklmnopqrstuvwxyz")

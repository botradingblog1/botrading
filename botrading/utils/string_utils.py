import hashlib


def create_md5_hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


def clean_string(s):
    if s is None or len(s) == 0:
        return ""
    return s.encode("ascii", "ignore").decode().strip()


def join_items(item_list):
    return ",".join(item_list)
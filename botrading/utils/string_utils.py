

def clean_string(s):
    if s is None or len(s) == 0:
        return ""
    return s.encode("ascii", "ignore").decode().strip()


def join_items(item_list):
    return ",".join(item_list)
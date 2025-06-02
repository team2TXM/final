# utils.py
def parse_date_range(date_range):
    if len(date_range) == 2:
        return str(date_range[0]), str(date_range[1])
    return None, None

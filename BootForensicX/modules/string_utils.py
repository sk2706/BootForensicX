import re

def extract_strings(data, min_length=6):

    pattern = rb"[ -~]{" + str(min_length).encode() + rb",}"

    return re.findall(pattern, data)
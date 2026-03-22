import math

def calculate_entropy(data):

    if not data:
        return 0

    frequency = {}

    for byte in data:
        frequency[byte] = frequency.get(byte, 0) + 1

    entropy = 0
    length = len(data)

    for count in frequency.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy
import hashlib
from modules.entropy_utils import calculate_entropy
from modules.string_utils import extract_strings

SECTOR_SIZE = 512

def analyze_mbr(f):

    print("\n====== LAYER 1: MBR ANALYSIS ======")

    f.seek(0)
    mbr = f.read(SECTOR_SIZE)

    print("MBR SHA256:", hashlib.sha256(mbr).hexdigest())
    print("MBR Entropy:", round(calculate_entropy(mbr), 4))

    signature = mbr[510:512]

    if signature == b'\x55\xAA':
        print("[✓] Valid MBR Signature (55AA)")
    else:
        print("[!] Invalid MBR Signature")

    strings_found = extract_strings(mbr)

    if strings_found:
        print("Potential MBR Strings:")
        for s in strings_found[:5]:
            print(" ", s.decode(errors="ignore"))
import hashlib
from modules.entropy_utils import calculate_entropy
from modules.string_utils import extract_strings

SECTOR_SIZE = 512


def analyze_vbr(f, offset):

    print("\n====== LAYER 2: VBR ANALYSIS ======")

    f.seek(offset)
    vbr = f.read(SECTOR_SIZE)

    print("VBR SHA256:", hashlib.sha256(vbr).hexdigest())
    print("VBR Entropy:", round(calculate_entropy(vbr), 4))

    if b"NTFS" in vbr:
        print("[✓] NTFS Signature Detected")
    else:
        print("[!] NTFS Signature Missing")

    strings_found = extract_strings(vbr)

    if strings_found:
        print("Potential VBR Strings:")
        for s in strings_found[:5]:
            print(" ", s.decode(errors="ignore"))


def analyze_boot_region(f, offset):

    print("\n====== LAYER 3: NTFS $Boot Region (16 sectors) ======")

    f.seek(offset)
    boot_region = f.read(SECTOR_SIZE * 16)

    print("$Boot SHA256:", hashlib.sha256(boot_region).hexdigest())
    print("$Boot Entropy:", round(calculate_entropy(boot_region), 4))

    strings_found = extract_strings(boot_region)

    if strings_found:
        print("Embedded Strings:")
        for s in strings_found[:10]:
            print(" ", s.decode(errors="ignore"))
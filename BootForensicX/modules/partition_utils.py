SECTOR_SIZE = 512

def detect_image_type(f):

    f.seek(3)
    sig = f.read(4)

    if sig == b"NTFS":
        return "logical"
    else:
        return "physical"


def get_partition_offset(f):

    f.seek(446)
    entry = f.read(16)

    start_lba = int.from_bytes(entry[8:12], byteorder="little")

    return start_lba * SECTOR_SIZE
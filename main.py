from modules.partition_utils import detect_image_type, get_partition_offset
from modules.mbr_analyzer import analyze_mbr
from modules.ntfs_analyzer import analyze_vbr, analyze_boot_region
from modules.file_carver import carve_files


def main():

    image_path = input("Enter path to disk image (.dd): ")

    with open(image_path, "rb") as f:

        image_type = detect_image_type(f)

        if image_type == "logical":

            print("\n[+] Logical NTFS Image Detected")
            partition_offset = 0

        else:

            print("\n[+] Physical Disk Image Detected")

            analyze_mbr(f)

            partition_offset = get_partition_offset(f)

            print(f"[+] Partition Offset Detected: {partition_offset} bytes")

        analyze_vbr(f, partition_offset)
        analyze_boot_region(f, partition_offset)

    carve_files(image_path)

    print("\n[+] Multi-Layer Boot Forensic Analysis Complete.")


if __name__ == "__main__":
    main()
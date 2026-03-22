def carve_files(image_path):

    print("\n====== LAYER 4: FILE CARVING ======")

    signatures = {
        "jpg": {
            "header": b'\xff\xd8\xff',
            "footer": b'\xff\xd9'
        },
        "pdf": {
            "header": b'%PDF',
            "footer": b'%%EOF'
        }
    }

    with open(image_path, "rb") as f:
        data = f.read()

    for filetype, sig in signatures.items():

        header = sig["header"]
        footer = sig["footer"]

        offset = 0
        count = 0

        while True:

            start = data.find(header, offset)

            if start == -1:
                break

            end = data.find(footer, start)

            if end == -1:
                break

            end += len(footer)

            file_data = data[start:end]

            filename = f"recovered_{count}.{filetype}"

            with open(filename, "wb") as out:
                out.write(file_data)

            print(f"[+] Recovered {filename} at offset {start}")

            count += 1
            offset = end
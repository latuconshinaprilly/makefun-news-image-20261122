"""THE SUNDAY SIGNAL — edisi Minggu dari @latuconshinaprilly3480 (Akun 18).

Penjaga rilis NI22 Wave 7: sebelum sinyal Minggu ini diteruskan, berkas
gambarnya ditimbang, dibaca ukurannya, dan dicocokkan hash-nya dua kali.
Kegagalan pada tahap mana pun menghentikan rilis dengan kode keluar 1.
"""

import hashlib
import os
import struct
import sys

CONCEPT = "THE SUNDAY SIGNAL"
ACCOUNT = "@latuconshinaprilly3480"
ACCOUNT_LABEL = "Akun 18"
BOUNTY = "news-image-20261122"
STORIES = 36
MAX_SIDE = 1024

SIGNATURE = b"\x89PNG\r\n\x1a\n"


def reject(why):
    print(f"ditolak: {why}", file=sys.stderr)
    return 1


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(root, "entry.png")
    if not os.path.isfile(src):
        return reject("entry.png tidak ada di folder ini")

    with open(src, "rb") as fp:
        prefix = fp.read(33)
    if len(prefix) != 33:
        return reject("prefix berkas kurang dari 33 byte")
    if prefix[:8] != SIGNATURE:
        return reject("signature PNG asing")
    if prefix[12:16] != b"IHDR":
        return reject("chunk IHDR tidak terdeteksi")
    dim_w, dim_h = struct.unpack(">II", prefix[16:24])
    if dim_w > MAX_SIDE or dim_h > MAX_SIDE:
        return reject(f"dimensi {dim_w}x{dim_h} menembus batas {MAX_SIDE}")

    raw = open(src, "rb").read()
    byte_count = len(raw)
    hash_value = hashlib.sha256(raw).hexdigest()

    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "entry.png")
    with open(target_file, "wb") as fp:
        fp.write(raw)

    reread = open(target_file, "rb").read()
    if len(reread) != byte_count:
        return reject("panjang salinan tidak sama dengan aslinya")
    if hashlib.sha256(reread).hexdigest() != hash_value:
        return reject("hash salinan tidak sama dengan aslinya")

    print(f"Concept: {CONCEPT}")
    print(f"Account: {ACCOUNT} ({ACCOUNT_LABEL})")
    print(f"Bounty: {BOUNTY}")
    print("File: entry.png")
    print(f"Size: {byte_count} bytes")
    print(f"Dim: {dim_w}x{dim_h}")
    print(f"SHA256: {hash_value}")
    print(f"Stories: {STORIES}")
    print("Copy verified byte-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

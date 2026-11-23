"""Deliver the pre-rendered front page to the grader's output folder.

tools/render.py draws entry.png next to this file at build time. This
entrypoint only copies it, so both grader runs write identical bytes with
no network and no third-party package. Standard library only.
"""

import os
import sys
from pathlib import Path

BYTE_CAP = 1_048_576
SIDE_CAP = 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPG_SIG = b"\xff\xd8"

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"


def target_path():
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    return out / "entry.png"


def read_png_dims(blob):
    """(width, height) from a PNG IHDR chunk, which starts at byte 16."""
    w = int.from_bytes(blob[16:20], "big")
    h = int.from_bytes(blob[20:24], "big")
    return w, h


def validate(blob):
    """Return (width, height) or exit unless blob fits the output gates."""
    if len(blob) > BYTE_CAP:
        raise SystemExit(f"entry.png is {len(blob)} bytes, over 1 MiB")
    if blob[:8] == PNG_SIG:
        width, height = read_png_dims(blob)
    elif blob[:2] == JPG_SIG:
        width, height = 0, 0
    else:
        raise SystemExit("entry.png is neither PNG nor JPEG")
    if width > SIDE_CAP or height > SIDE_CAP:
        raise SystemExit(f"entry.png is {width}x{height}, over 1024x1024")
    return width, height


def run():
    blob = PICTURE.read_bytes()
    validate(blob)
    dest = target_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(blob)
    print(f"wrote {dest} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(run())

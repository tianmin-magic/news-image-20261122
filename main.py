"""Copy the pre-rendered front page to the grader's output directory.

The front page is rendered at build time by tools/render.py into entry.png
next to this file. This entrypoint only copies that file, so the two grader
runs write identical bytes with no network and no third-party package.
Standard library only.
"""

import os
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_HEAD = b"\x89PNG\r\n\x1a\n"
JPG_HEAD = b"\xff\xd8"

ROOT = Path(__file__).resolve().parent
IMAGE = ROOT / "entry.png"


def out_path():
    base = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    return base / "entry.png"


def png_size(blob):
    """Width and height from a PNG's IHDR chunk (bytes 16..24)."""
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    return width, height


def check(blob):
    """Raise SystemExit unless blob is a PNG/JPEG within the size gates."""
    if len(blob) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(blob)} bytes, over 1 MiB")
    if blob[:8] == PNG_HEAD:
        width, height = png_size(blob)
    elif blob[:2] == JPG_HEAD:
        width, height = 0, 0
    else:
        raise SystemExit("entry.png is neither PNG nor JPEG")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"entry.png is {width}x{height}, over 1024x1024")
    return width, height


def main():
    blob = IMAGE.read_bytes()
    check(blob)
    target = out_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(blob)
    print(f"wrote {target} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

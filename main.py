"""Entrypoint for make.fun news-image-20261126.

Copies the bundled front-page image (entry.png, rendered beforehand
by build_image.py) to the output directory as entry.png.

Standard library only, no network, no clock, no randomness:
running it twice writes byte-identical output.
"""

import os
import shutil
import sys


def output_dir():
    """Where the image goes: $MAKEFUN_OUTPUT_DIR, else /output."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return chosen


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1

    with open(source, "rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1

    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    size = os.path.getsize(target)
    print("wrote", target, "(%d bytes)" % size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""news-image-20261117 entry program.

Deterministic and offline by design: it simply copies the bundled
``entry.png`` (rendered ahead of time by ``build/render.py``) to
``/output/entry.png``. No network, no clock, no randomness — running it
any number of times produces byte-identical output.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def main() -> None:
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Apply the repository's readable source patches to an extracted web-build tree."""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PATCH = REPOSITORY_ROOT / "patches" / "recipe-gui-wheel-scroll.patch"
PATCHED_FILES = (
    "src/client/gui/Screen.h",
    "src/client/gui/Screen.cpp",
    "src/client/gui/components/ScrollingPane.h",
    "src/client/gui/components/ScrollingPane.cpp",
    "src/client/gui/screens/crafting/PaneCraftingScreen.h",
    "src/client/gui/screens/crafting/PaneCraftingScreen.cpp",
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "web_build_root",
        type=Path,
        help="Path to the extracted web-build directory containing src/",
    )
    args = parser.parse_args()
    if not (args.web_build_root / "src").is_dir():
        parser.error(f"{args.web_build_root / 'src'} does not exist")

    # The archived source uses CRLF; normalize only patched files so the readable
    # patch applies consistently on all platforms.
    for relative_path in PATCHED_FILES:
        path = args.web_build_root / relative_path
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))

    subprocess.run(
        ["patch", "--batch", "--forward", "-p1", "-i", str(PATCH)],
        cwd=args.web_build_root,
        check=True,
    )


if __name__ == "__main__":
    main()

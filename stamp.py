"""Stamp every image link in README.md with its file's content hash.

GitHub and browsers cache an image by its URL, so a re-rendered banner
or card kept showing the old picture. Each `assets/...` link gets
`?v=<first 8 hex of the file's sha1>`: a changed file gets a new URL,
an unchanged one keeps its URL and its cache. make.py and projects.py
call this after they render; `python3 stamp.py` does it by hand.
"""
import hashlib
import re
from pathlib import Path

HERE = Path(__file__).parent
LINK = re.compile(r'(?P<path>assets/[\w./-]+\.(?:svg|png|webp|gif|jpg))(?:\?v=[0-9a-f]+)?(?=")')


def stamp_readme() -> int:
    readme = HERE / "README.md"
    text = readme.read_text()

    def versioned(m: re.Match) -> str:
        path = HERE / m["path"]
        if not path.exists():
            return m.group(0)
        return f'{m["path"]}?v={hashlib.sha1(path.read_bytes()).hexdigest()[:8]}'

    stamped, n = LINK.subn(versioned, text)
    readme.write_text(stamped)
    return n


if __name__ == "__main__":
    print(f"README: {stamp_readme()} image links stamped")

"""process a src string and remove comments"""

import re


def process(src: str) -> str:
    return re.sub(r"[^<>+-,.\[\]]", '', src)

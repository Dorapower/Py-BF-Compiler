"""process a src string and remove comments"""

import re


def preprocess(src: str) -> str:
    return re.sub(r"[^<>+-,.\[\]]", '', src)

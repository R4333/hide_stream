# -*- coding: utf-8 -*-
"""
    stego_lsb.StegDetect
    ~~~~~~~~~~~~~~~~~~~~

    This module contains functions for detecting images
    which have been modified using the functions from
    the module :mod:`stego_lsb.LSBSteg`.

    :copyright: (c) 2015 by R433.
    :license: MIT License, see LICENSE.md for more details.
"""
import logging
import os
from time import time
from typing import cast, Tuple, Iterable

from PIL import Image

log = logging.getLogger(__name__)


def show_lsb(image_path: str, n: int) -> None:
    """Shows the n least significant bits of image"""
    if image_path is None:
        raise ValueError("StegDetect requires an input image file path")

    start = time()
    with Image.open(image_path) as image:
        # Used to set everything but the least significant n bits to 0 when
        # using bitwise AND on an integer
        mask = (1 << n) - 1

        image_data = cast(Iterable[Tuple[int, int, int]], image.getdata())
        color_data = [
            (255 * ((rgb[0] & mask) + (rgb[1] & mask) + (rgb[2] & mask)) // (3 * mask),) * 3
            for rgb in image_data
        ]

        image.putdata(color_data)
        log.debug(f"Runtime: {time() - start:.2f}s")
        file_name, file_extension = os.path.splitext(image_path)
        image.save(f"{file_name}_{n}LSBs{file_extension}")

"""Reads the small uncompressed BMP files the games load onto the LEDs.

The real library uses Pillow; this needs nothing, so the same code runs in
the browser. It handles the 1, 4, 8, 24 and 32 bit images an image editor
saves, and returns a list of [r, g, b] in the order set_pixels() takes.
"""

import struct


def read_bmp(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"BM":
        raise ValueError(f"{path} is not a BMP file")
    offset = struct.unpack_from("<I", data, 10)[0]
    header = struct.unpack_from("<I", data, 14)[0]
    width, height = struct.unpack_from("<ii", data, 18)
    bits = struct.unpack_from("<H", data, 28)[0]
    compression = struct.unpack_from("<I", data, 30)[0]
    if compression not in (0, 3):
        raise ValueError(f"{path}: compressed BMPs are not supported")
    colours = struct.unpack_from("<I", data, 46)[0] if header >= 40 else 0
    palette = []
    if bits <= 8:
        count = colours or (1 << bits)
        base = 14 + header
        for i in range(count):
            b, g, r = data[base + i * 4: base + i * 4 + 3]
            palette.append([r, g, b])
    top_down = height < 0
    height = abs(height)
    stride = (width * bits + 31) // 32 * 4
    pixels = []
    for row in range(height):
        y = row if top_down else height - 1 - row
        line = data[offset + y * stride: offset + (y + 1) * stride]
        for x in range(width):
            if bits == 24 or bits == 32:
                step = bits // 8
                b, g, r = line[x * step: x * step + 3]
                pixels.append([r, g, b])
            else:
                bit = x * bits
                value = (line[bit // 8] >> (8 - bits - bit % 8)) & ((1 << bits) - 1)
                pixels.append(list(palette[value]))
    return pixels

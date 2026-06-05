from array import array
from typing import BinaryIO

UINT32_TYPE_CODE = "I"
UINT32_SIZE = 4


def ensure_uint32_supported() -> None:
    """Check that array('I') is represented as 32-bit unsigned integers."""
    if array(UINT32_TYPE_CODE).itemsize != UINT32_SIZE:
        raise RuntimeError("array('I') is not 32-bit on this platform.")


def read_uint32_chunk(file: BinaryIO, count: int) -> array:
    """Read up to count uint32 numbers from the current file position.

    Returns an array('I'). If the end of file is reached, it may return
    fewer than count numbers.
    """
    numbers = array(UINT32_TYPE_CODE)

    try:
        numbers.fromfile(file, count)
    except EOFError:
        pass

    return numbers


def write_uint32_chunk(file: BinaryIO, numbers: array) -> None:
    """Write uint32 numbers to a binary file."""
    numbers.tofile(file)

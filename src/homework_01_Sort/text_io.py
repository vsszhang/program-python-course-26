from array import array
from pathlib import Path

from .binary_io import UINT32_TYPE_CODE, read_uint32_chunk, write_uint32_chunk


def text_to_binary(
    text_path: Path,
    binary_path: Path,
    buffer_size: int = 100_000,
) -> None:
    """Convert a text file with unsigned 32-bit integers into a binary file."""
    buffer = array(UINT32_TYPE_CODE)

    with (
        text_path.open("r", encoding="utf-8") as text_file,
        binary_path.open("wb") as binary_file,
    ):
        for line in text_file:
            for token in line.split():
                number = int(token)
                if number < 0 or number > 2**32 - 1:
                    raise ValueError(f"Number is out of uint32 range: {number}")

                buffer.append(number)

                if len(buffer) >= buffer_size:
                    write_uint32_chunk(binary_file, buffer)
                    buffer = array(UINT32_TYPE_CODE)

        if len(buffer) > 0:
            write_uint32_chunk(binary_file, buffer)


def binary_to_text(
    binary_path: Path,
    text_path: Path,
    chunk_size: int = 100_000,
) -> None:
    """Convert a binary file with unsigned 32-bit integers into a text file."""
    with (
        binary_path.open("rb") as binary_file,
        text_path.open("w", encoding="utf-8") as text_file,
    ):
        while True:
            numbers = read_uint32_chunk(binary_file, chunk_size)

            if len(numbers) == 0:
                break

            for number in numbers:
                text_file.write(f"{number}\n")

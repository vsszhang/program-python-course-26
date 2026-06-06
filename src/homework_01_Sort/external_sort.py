import heapq
import math
import os
from array import array
from multiprocessing import Pool
from pathlib import Path
from tempfile import TemporaryDirectory

from .binary_io import (
    UINT32_SIZE,
    UINT32_TYPE_CODE,
    read_uint32_chunk,
    write_uint32_chunk,
)


def sort_numbers(numbers: array) -> array:
    """Sort uint32 numbers and return a new array."""
    return array(UINT32_TYPE_CODE, sorted(numbers))


def get_number_count(input_path: Path) -> int:
    """Return the number of uint32 values stored in the binary file."""
    file_size = input_path.stat().st_size

    if file_size % UINT32_SIZE != 0:
        raise ValueError("Input file size is not divisible by uint32 size.")

    return file_size // UINT32_SIZE


def sort_chunk_by_index(args: tuple[Path, int, int, Path]) -> Path:
    """Read, sort and write one chunk of the input file.

    This function is executed inside worker processes.
    Each worker loads no more than its assigned worker chunk size into memory.
    """
    input_path, chunk_index, chunk_size, temp_dir = args
    offset = chunk_index * chunk_size * UINT32_SIZE

    with input_path.open("rb") as input_file:
        input_file.seek(offset)
        numbers = read_uint32_chunk(input_file, chunk_size)

    sorted_numbers = sort_numbers(numbers)
    chunk_path = temp_dir / f"chunk_{chunk_index:06d}.bin"

    with chunk_path.open("wb") as chunk_file:
        write_uint32_chunk(chunk_file, sorted_numbers)

    return chunk_path


def split_and_sort_chunks(
    input_path: Path,
    chunk_size: int,
    temp_dir: Path,
) -> list[Path]:
    """Split a binary file into sorted chunk files using all CPU cores."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    number_count = get_number_count(input_path)
    if number_count == 0:
        return []

    worker_count = min(os.cpu_count() or 1, chunk_size, number_count)
    worker_chunk_size = max(1, chunk_size // worker_count)
    chunk_count = math.ceil(number_count / worker_chunk_size)

    # The input chunk_size is treated as the total number of values that may be
    # loaded into memory at the same time by all worker processes together.

    tasks = [
        (input_path, chunk_index, worker_chunk_size, temp_dir)
        for chunk_index in range(chunk_count)
    ]

    with Pool(processes=worker_count) as pool:
        chunk_paths = pool.map(sort_chunk_by_index, tasks)

    return sorted(chunk_paths)


def calculate_merge_buffer_sizes(chunk_size: int, chunk_count: int) -> tuple[int, int]:
    """Calculate input and output buffer sizes for the merge stage.

    About half of the allowed memory is uesd for input buffers, and the rest is
    used for the output buffer. Buffer sizes are measured in numbers, not bytes.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    if chunk_count <= 0:
        return 1, chunk_size

    input_memory_limit = max(1, chunk_size // 2)
    input_buffer_size = max(1, input_memory_limit // chunk_count)
    output_buffer_size = max(1, chunk_size - input_buffer_size * chunk_count)

    return input_buffer_size, output_buffer_size


def merge_sorted_chunks(
    chunk_paths: list[Path],
    output_path: Path,
    input_buffer_size: int,
    output_buffer_size: int,
) -> None:
    """Merge sorted chunk files into one sorted binary output file.

    Each input chunk file is read by small buffers instead of reading one number
    from disk at a time. The heap stores only the current candidate number from
    each chunk.
    """
    input_files = [chunk_path.open("rb") for chunk_path in chunk_paths]
    input_buffers: list[array] = []
    input_positions: list[int] = []
    heap: list[tuple[int, int]] = []
    output_buffer = array(UINT32_TYPE_CODE)

    try:
        for file_index, input_file in enumerate(input_files):
            buffer = read_uint32_chunk(input_file, input_buffer_size)
            input_buffers.append(buffer)
            input_positions.append(0)

            if len(buffer) > 0:
                heapq.heappush(heap, (buffer[0], file_index))
                input_positions[file_index] = 1

        with output_path.open("wb") as output_file:
            while heap:
                number, file_index = heapq.heappop(heap)
                output_buffer.append(number)

                if len(output_buffer) >= output_buffer_size:
                    write_uint32_chunk(output_file, output_buffer)
                    output_buffer = array(UINT32_TYPE_CODE)

                if input_positions[file_index] >= len(input_buffers[file_index]):
                    input_buffers[file_index] = read_uint32_chunk(
                        input_files[file_index],
                        input_buffer_size,
                    )
                    input_positions[file_index] = 0

                if input_positions[file_index] < len(input_buffers[file_index]):
                    next_number = input_buffers[file_index][input_positions[file_index]]
                    input_positions[file_index] += 1
                    heapq.heappush(heap, (next_number, file_index))

            if len(output_buffer) > 0:
                write_uint32_chunk(output_file, output_buffer)
    finally:
        for input_file in input_files:
            input_file.close()


def external_sort(
    input_path: Path,
    output_path: Path,
    chunk_size: int,
) -> None:
    """Sort a binary uint32 file using external merge sort.

    The input `chunk_size` is interpreted as the total number of values that may
    be loaded into memory at the same time during the parallel chunk-sorting stage.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    with TemporaryDirectory(dir=input_path.parent) as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        chunk_paths = split_and_sort_chunks(input_path, chunk_size, temp_dir)
        input_buffer_size, output_buffer_size = calculate_merge_buffer_sizes(
            chunk_size=chunk_size,
            chunk_count=len(chunk_paths),
        )
        merge_sorted_chunks(
            chunk_paths, output_path, input_buffer_size, output_buffer_size
        )

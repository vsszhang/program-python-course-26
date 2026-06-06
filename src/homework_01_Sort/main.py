from argparse import ArgumentParser
from pathlib import Path

from src.homework_01_Sort.binary_io import ensure_uint32_supported
from src.homework_01_Sort.external_sort import external_sort
from src.homework_01_Sort.text_io import binary_to_text, text_to_binary

INPUT_BINARY_NAME = "input.bin"
OUTPUT_BINARY_NAME = "sorted_input.bin"
OUTPUT_TEXT_NAME = "sorted_input.txt"


def parse_args():
    parser = ArgumentParser(description="External merge sort for uint32 numbers.")

    parser.add_argument(
        "input_file",
        help="Path to the input text file containing uint32 numbers.",
    )

    parser.add_argument(
        "chunk_size",
        type=int,
        help="Maximum number of values allowed in memory at the same time.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    ensure_uint32_supported()

    input_text_path = Path(args.input_file).resolve()

    if not input_text_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_text_path}")

    working_dir = input_text_path.parent

    input_binary_path = working_dir / INPUT_BINARY_NAME
    output_binary_path = working_dir / OUTPUT_BINARY_NAME
    output_text_path = working_dir / OUTPUT_TEXT_NAME

    print("[1/3] Converting text file to binary...")
    text_to_binary(input_text_path, input_binary_path)

    print("[2/3] Performing external merge sort...")
    external_sort(
        input_path=input_binary_path,
        output_path=output_binary_path,
        chunk_size=args.chunk_size,
    )

    print("[3/3] Converting sorted binary file to text...")
    binary_to_text(output_binary_path, output_text_path)

    print("Done.")
    print(f"Sorted binary file: {output_binary_path}")
    print(f"Sorted text file:   {output_text_path}")


if __name__ == "__main__":
    main()

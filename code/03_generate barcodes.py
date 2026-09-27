"""Write barcodes from an explicitly selected input file and output directory."""
import argparse
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input file with one value per line")
    parser.add_argument("output", type=Path, help="Directory for generated images")
    args = parser.parse_args(argv)

    import barcode
    from barcode.writer import ImageWriter

    args.output.mkdir(parents=True, exist_ok=True)
    with args.input.open(encoding="utf-8") as source:
        for line in source:
            value = line.strip()
            if not value:
                continue
            if value in (".", "..") or any(mark in value for mark in ("/", "\\", ":")):
                raise ValueError("Input values must be filenames, not paths")
            code39 = barcode.get("code39", value, writer=ImageWriter(), add_checksum=False)
            code39.save(str(args.output / value))


if __name__ == "__main__":
    main()


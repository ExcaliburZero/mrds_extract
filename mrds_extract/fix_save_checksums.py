import argparse
import logging
import pathlib
import sys
from dataclasses import dataclass

from mrds_util.raw import Checksums, SaveFile

SUCCESS = 0


@dataclass(frozen=True)
class Args:
    filepath: pathlib.Path


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("filepath", type=pathlib.Path)

    return parser


def setup_logger(logger: logging.Logger) -> None:
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(levelname)s> %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def main(argv: list[str]) -> int:
    logger = logging.getLogger()
    setup_logger(logger)

    parser = create_arg_parser()
    args = Args(**vars(parser.parse_args(argv)))  # ty: ignore[missing-argument]

    with args.filepath.open("rb") as input_stream:
        save_file = SaveFile.from_bin(input_stream)

    before_checksums: list[Checksums] = []
    after_checksums: list[Checksums] = []
    for save_entry in save_file.entries:
        before_checksums.append(
            Checksums(
                header_checksum=save_entry.header_checksum, body_checksum=save_entry.body_checksum
            )
        )

        save_entry.update_checksums()

        after_checksums.append(
            Checksums(
                header_checksum=save_entry.header_checksum, body_checksum=save_entry.body_checksum
            )
        )

    first_correct = before_checksums[0] == after_checksums[0]
    second_correct = before_checksums[1] == after_checksums[1]
    if first_correct and second_correct:
        logger.info("All checksums are already correct.")
    else:
        logger.info("Updated checksums:")
        for i, th in [(0, "1st"), (1, "2nd")]:
            if before_checksums[i].header_checksum != after_checksums[i].header_checksum:
                logger.info(
                    f"  {th} header checksum from {before_checksums[i].header_checksum:#010x} to {after_checksums[i].header_checksum:#010x}"
                )

            if before_checksums[i].body_checksum != after_checksums[i].body_checksum:
                logger.info(
                    f"  {th} body   checksum from {before_checksums[i].body_checksum:#010x} to {after_checksums[i].body_checksum:#010x}"
                )

    with args.filepath.open("wb") as output_stream:
        save_file.write_bin(output_stream)
    logger.info(f"Wrote updated save file to: {args.filepath}")

    return SUCCESS


def main_without_args() -> int:
    return main(sys.argv[1:])

import argparse
import logging
import pathlib
import sys
from dataclasses import dataclass

from mrds_util.raw import SaveFile

SUCCESS = 0


@dataclass(frozen=True)
class Args:
    save_file: list[pathlib.Path]


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("--save_file", type=pathlib.Path, nargs="+", required=True)

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

    for save_file_path in args.save_file:
        with save_file_path.open("rb") as input_stream:
            save_file = SaveFile.from_bin(input_stream)

        logger.info(save_file)

    return SUCCESS


def main_without_args() -> int:
    return main(sys.argv[1:])

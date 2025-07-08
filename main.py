import argparse
import json
import logging
import pathlib
import sys
from dataclasses import asdict, dataclass
from typing import Any

from mrds_util.raw import SaveFile

SUCCESS = 0


@dataclass(frozen=True)
class Args:
    input: pathlib.Path
    output: pathlib.Path


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)

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

    with args.input.open("rb") as input_stream:
        save_file = SaveFile.from_bin(input_stream)

    with args.output.open("wb") as output_stream:
        save_file.write_bin(output_stream)

    return SUCCESS


def jsonize(obj: Any) -> Any:
    if isinstance(obj, list):
        return [jsonize(o) for o in obj]
    elif isinstance(obj, dict):
        return {jsonize(k): jsonize(v) for k, v in obj.items()}
    elif isinstance(obj, bytes):
        return str(obj)

    return obj


def main_without_args() -> int:
    return main(sys.argv[1:])

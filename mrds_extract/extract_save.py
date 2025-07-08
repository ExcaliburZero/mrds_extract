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

        for save_entry in save_file.entries:
            # save_entry.monsters[0].power = 999
            print("====BEFORE:", save_entry.calculate_checksum())
            print("save_entry.ranch_name:", save_entry.ranch_name, save_entry.checksum)
            # save_entry.ranch_name = "Undertale".encode("ascii")
            save_entry.monsters[0].power = 999
            print("save_entry.ranch_name:", save_entry.ranch_name)
            print("====AFTER:", save_entry.calculate_checksum())
            save_entry.update_checksum()
            print("====AFTER UPDATE:", save_entry.calculate_checksum(), save_entry.checksum)

        # print(save_file.entries[0].monsters[0].power)

        # with save_file_path.open("rb") as input_stream:
        #    input_stream.read(30 + 64)
        #    s = 0
        #    for _ in range(0, int((15524 - 0) / 4)):
        #        c = int.from_bytes(input_stream.read(4), "little")
        #        s = (s + c) & 0xFFFFFFFF

        # logger.info(save_file)
        # logger.info(f"{save_file.entries[0].calculate_checksum():#010x}")

        output_filepath = save_file_path.with_name("updated.sav")
        with output_filepath.open("wb") as output_stream:
            save_file.write_bin(output_stream)
        logger.info(f"Wrote updated save file to: {output_filepath}")

        # logger.info(s.to_bytes(4, "little"))

    return SUCCESS


def main_without_args() -> int:
    return main(sys.argv[1:])

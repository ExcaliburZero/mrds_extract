from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Annotated

import dataclasses_struct as dcs

from mrds_util.raw._monster import Monster
from mrds_util.raw._save_file_checksum_mapping import SAVE_FILE_CHECKSUM_MAPPING
from mrds_util.raw._util import BinaryReadWriteable

SAVE_ENTRY_HEADER_SIZE = 56
SAVE_ENTRY_HEADER_PLUS_BODY_SIZE = 0x3CDC


@dataclass(frozen=True)
class Checksums:
    header_checksum: int
    body_checksum: int


@dcs.dataclass_struct(size="std", byteorder="little")
class SaveEntry(BinaryReadWriteable):
    unknown_a: Annotated[bytes, 10]
    ranch_name: Annotated[bytes, 13]
    unknown_b: Annotated[bytes, 4]
    player_name: Annotated[bytes, 13]
    unknown_c: Annotated[bytes, 16]
    header_checksum: dcs.U32
    unknown_d: Annotated[bytes, 292]
    gold: dcs.U32
    unknown_e: Annotated[bytes, 100]
    monsters: Annotated[list[Monster], 31]  # Current monster, then 30 in storage
    unknown_f: Annotated[bytes, 2104]
    body_checksum: dcs.U32

    def update_checksums(self) -> None:
        checksums = self.calculate_checksums()
        self.header_checksum = checksums.header_checksum
        self.body_checksum = checksums.body_checksum

    def calculate_checksums(self) -> Checksums:
        # Write the data to a bytearray so that we can read the bytes sequentially and update the
        # header checksum without actually mutating `self``
        output_stream = io.BytesIO()
        self.write_bin(output_stream)
        data = bytearray(output_stream.getbuffer())

        # Checksum the header data
        checksum = 0xFFFFFFFF
        for byte in data[:SAVE_ENTRY_HEADER_SIZE]:
            lookup = SAVE_FILE_CHECKSUM_MAPPING[(checksum ^ byte) & 0xFF]
            checksum = lookup ^ checksum >> 8

        header_checksum = checksum ^ 0xFFFFFFFF

        # Update the header checksum in the data, since it is processed as a part of the body
        # checksum
        data[56:60] = header_checksum.to_bytes(4, "little")

        # Checksum the header + body
        checksum = 0xFFFFFFFF
        for byte in data[:SAVE_ENTRY_HEADER_PLUS_BODY_SIZE]:
            lookup = SAVE_FILE_CHECKSUM_MAPPING[(checksum ^ byte) & 0xFF]
            checksum = lookup ^ checksum >> 8

        checksum = checksum ^ 0xFFFFFFFF

        return Checksums(header_checksum=header_checksum, body_checksum=checksum)


@dcs.dataclass_struct(size="std", byteorder="little")
class SaveFile(BinaryReadWriteable):
    """
    Representation of a "*.sav" save file for the game.

    The save file has two SaveEntry sections. Likely this was done as a save data corruption
    mitigation strategy. In case the game is powered off in the middle of a save, only one of the
    two SaveEntries will be partially written (and thus potentially corrupted). The game can detect
    via checksums if one of the SaveEntries is corrupted, and if so use the other SaveEntry. If
    both are corrupted, then the game clears the save data.
    """

    header: Annotated[bytes, 34]  # Game name twice?
    entries: Annotated[list[SaveEntry], 2]

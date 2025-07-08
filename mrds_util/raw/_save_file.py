from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Annotated

import dataclasses_struct as dcs
import numpy as np

from mrds_util.raw._monster import Monster
from mrds_util.raw._save_file_checksum_mapping import SAVE_FILE_CHECKSUM_MAPPING
from mrds_util.raw._util import BinaryReadWriteable

# Note: There appears to be 2 copies of save data in the save file and they appear to checked
# against a checksum on start. Haven't fully tested the game's behavior, but it seems to load/use
# use whichever one passes the checksum and if both fail the checksum then it resets the save data
# (need to fully confirm this).
#
# When loading the game, the save data is stored at 0x023CE978, checksum is at 0x023CE9B0. The data
# is only there briefly after clicking continue but before being overwritten. Maybe its even
# overwritten on game successful load?
#
# The checksum does not appear to take into account data before it in the save entry.
#  * Nah, I think it looks at some earlier data? Saving and then re-saving results in different
#    checksums

#
# More checksum locations?
#  * 0x023DFFB8
#  * 0x023DFFF4
#  * 0x021AF078
#
# Maybe the data load or checksum happens in the ARM7 binary?
#
# Game does hit 0x020b4848 on startup
#
# First byte of unknown_a is incremented twice before checksumming for who knows what reason...

SAVE_ENTRY_HEADER_SIZE = 56
SAVE_ENTRY_HEADER_PLUS_BODY_SIZE = 0x3CDC


@dataclass
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
    unknown_d: Annotated[bytes, 396]
    monsters: Annotated[list[Monster], 31]  # Current monster, then 30 in storage
    unknown_e: Annotated[bytes, 2104]
    body_checksum: dcs.U32

    def update_checksums(self) -> None:
        checksums = self.calculate_checksums()
        self.header_checksum = checksums.header_checksum
        self.body_checksum = checksums.body_checksum

    def calculate_checksums(self) -> Checksums:
        checksum: int = 0xFFFFFFFF

        output_stream = io.BytesIO()
        self.write_bin(output_stream)
        data = bytearray(output_stream.getbuffer())

        # Checksum the header data
        for byte in data[:SAVE_ENTRY_HEADER_SIZE]:
            lookup = SAVE_FILE_CHECKSUM_MAPPING[(checksum ^ byte) & 0xFF]
            checksum = int(np.uint32(lookup) ^ np.uint32(checksum) >> 8)

        header_checksum = int(np.uint32(checksum) ^ 0xFFFFFFFF)

        # Update the header checksum in the data, since it is processed as a part of the body
        # checksum
        data[56:60] = header_checksum.to_bytes(4, "little")

        # Checksum the header + body
        checksum: int = 0xFFFFFFFF
        for byte in data[:SAVE_ENTRY_HEADER_PLUS_BODY_SIZE]:
            lookup = SAVE_FILE_CHECKSUM_MAPPING[(checksum ^ byte) & 0xFF]
            checksum = int(np.uint32(lookup) ^ np.uint32(checksum) >> 8)

        checksum = int(np.uint32(checksum) ^ 0xFFFFFFFF)

        return Checksums(header_checksum=header_checksum, body_checksum=checksum)


@dcs.dataclass_struct(size="std", byteorder="little")
class SaveFile(BinaryReadWriteable):
    header: Annotated[bytes, 34]  # Game name twice?
    entries: Annotated[list[SaveEntry], 2]

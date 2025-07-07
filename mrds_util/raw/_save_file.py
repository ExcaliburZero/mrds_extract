from __future__ import annotations

from typing import Annotated

import dataclasses_struct as dcs

from mrds_util.raw._monster import Monster
from mrds_util.raw._util import BinaryReadWriteable

# Note: There appears to be 2 copies of save data in the save file and they appear to checked
# against a checksum on start. Haven't fully tested the game's behavior, but it seems to load/use
# use whichever one passes the checksum and if both fail the checksum then it resets the save data
# (need to fully confirm this).
#
# When loading the game, the save data is stored at 0x023CE978


@dcs.dataclass_struct(size="std", byteorder="little")
class SaveEntry:
    unknown_a: Annotated[bytes, 10]
    ranch_name: Annotated[bytes, 13]
    unknown_b: Annotated[bytes, 4]
    player_name: Annotated[bytes, 13]
    unknown_c: Annotated[bytes, 416]
    monsters: Annotated[list[Monster], 31]  # Current monster, then 30 in storage


@dcs.dataclass_struct(size="std", byteorder="little")
class SaveFile(BinaryReadWriteable):
    header: Annotated[bytes, 34]  # Game name twice?
    entries: Annotated[list[SaveEntry], 2]

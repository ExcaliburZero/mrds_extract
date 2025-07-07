from typing import Annotated

import dataclasses_struct as dcs

from mrds_util.raw._monster import Monster
from mrds_util.raw._util import BinaryReadWriteable


@dcs.dataclass_struct(size="std", byteorder="little")
class SaveFile(BinaryReadWriteable):
    header: Annotated[bytes, 44]  # Game name twice?
    ranch_name: Annotated[bytes, 17]
    player_name: Annotated[bytes, 17]
    unknown_a: Annotated[bytes, 412]
    monsters: Annotated[list[Monster], 2]  # TODO: find out correct number
